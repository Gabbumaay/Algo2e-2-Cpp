import React, { useEffect, useRef, useState } from "react";
import axios from "axios";

const VALID_TYPES = [
  "int",
  "float",
  "string",
  "long",
  "char",
  "array",
  "vector",
  "set",
  "set_int",
  "set_float",
  "set_double",
  "set_char",
  "set_string",
];

const DEFAULT_CODE =
  "\\Fn Tournament() {\n    b \\gets a + 1;\n    \\While (a < b) {\n        \\If (a < 5) {\n            \\KwRet b;\n        }\n    }\n}\n";
const CODE_STORAGE_KEY = "pseudoToCpp.code";

function App() {
  const [code, setCode] = useState(() => {
    const saved = localStorage.getItem(CODE_STORAGE_KEY);
    return saved ?? DEFAULT_CODE;
  });
  const [cpp, setCpp] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState(null);
  const toastTimerRef = useRef(null);
  const [backendOnline, setBackendOnline] = useState(true);

  // Tracks previously chosen datatypes so the backend never has to ask on stdin.
  const [typeHints, setTypeHints] = useState({});

  // When the backend reports a missing type, we surface a prompt in the UI.
  const [pendingVar, setPendingVar] = useState(null);
  const [selectedType, setSelectedType] = useState(VALID_TYPES[0]);

  // Toggle for middle TYPE MAP panel
  const [showTypeMap, setShowTypeMap] = useState(false);

  const sendConvertRequest = async (currentCode, currentHints) => {
    const res = await axios.post("http://localhost:5000/convert", {
      code: currentCode,
      types: currentHints,
    });
    return res.data;
  };

  const checkBackend = async () => {
    try {
      const res = await axios.get("http://localhost:5000/health", {
        timeout: 1200,
      });
      const healthy = res?.data?.status === "ok";
      if (!healthy) {
        setBackendOnline(false);
        return false;
      }
      setBackendOnline(true);
      setError((prev) => (prev.startsWith("Backend is offline") ? "" : prev));
      return true;
    } catch {
      setBackendOnline(false);
      return false;
    }
  };

  const handleConvert = async () => {
    if (!backendOnline) {
      setError("Backend is offline. Please start server.py and try again.");
      setToast({
        type: "error",
        message: "Backend is offline",
        position: "center",
      });
      setPendingVar(null);
      // Refresh status in background without delaying the toast.
      checkBackend();
      return;
    }

    const online = await checkBackend();
    if (!online) {
      setError("Backend is offline. Please start server.py and try again.");
      setToast({
        type: "error",
        message: "Backend is offline",
        position: "center",
      });
      setPendingVar(null);
      return;
    }

    setLoading(true);
    setError("");
    setCpp("");
    setPendingVar(null);
    try {
      const data = await sendConvertRequest(code, typeHints);
      setCpp(data.cpp || "");
    } catch (err) {
      const resp = err.response?.data;
      if (resp?.error === "missing_type" && resp.variable) {
        // Ask for the datatype in the frontend instead of the terminal.
        setPendingVar(resp.variable);
        setSelectedType((prev) => prev || VALID_TYPES[0]);
        setError("");
      } else {
        const msg = resp?.error || err.message || "Unknown error";
        setError(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmType = async () => {
    if (!pendingVar || !selectedType) return;
    const updatedHints = {
      ...typeHints,
      [pendingVar]: selectedType,
    };
    setTypeHints(updatedHints);
    setPendingVar(null);
    setError("");
    setLoading(true);
    setCpp("");
    try {
      const data = await sendConvertRequest(code, updatedHints);
      setCpp(data.cpp || "");
    } catch (err) {
      const resp = err.response?.data;
      if (resp?.error === "missing_type" && resp.variable) {
        setPendingVar(resp.variable);
        setSelectedType((prev) => prev || VALID_TYPES[0]);
        setError("");
      } else {
        const msg = resp?.error || err.message || "Unknown error";
        setError(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(cpp);
      setToast({ type: "success", message: "C++ code copied to clipboard" });
    } catch (e) {
      setToast({ type: "error", message: "Failed to copy" });
    }
  };

  useEffect(() => {
    localStorage.setItem(CODE_STORAGE_KEY, code);
  }, [code]);

  useEffect(() => {
    let active = true;

    const poll = async () => {
      const ok = await checkBackend();
      if (!active) return;
      if (!ok && !loading) {
        setError(
          (prev) => prev || "Backend is offline. Please start server.py.",
        );
      }
    };

    poll();
    const intervalId = setInterval(poll, 10000);
    return () => {
      active = false;
      clearInterval(intervalId);
    };
  }, [loading]);

  useEffect(() => {
    if (!toast) return;
    if (toastTimerRef.current) {
      clearTimeout(toastTimerRef.current);
    }
    toastTimerRef.current = setTimeout(() => {
      setToast(null);
    }, 2200);
    return () => {
      if (toastTimerRef.current) {
        clearTimeout(toastTimerRef.current);
      }
    };
  }, [toast]);

  return (
    <div className="app-root">
      {toast && (
        <div
          className={`toast ${toast.type} ${toast.position === "center" ? "center" : ""}`}
          role="status"
          aria-live="polite"
        >
          <span className="toast-dot" aria-hidden="true" />
          <span className="toast-message">{toast.message}</span>
          <button
            className="toast-close"
            onClick={() => setToast(null)}
            aria-label="Dismiss"
          >
            ×
          </button>
        </div>
      )}
      <div className="app-shell">
        <header className="app-header">
          <h1>Pseudo ➜ C++ Converter</h1>
          <p>
            Write your pseudo-code on the left and generate C++ on the right.
          </p>
          <p className={`status-line ${backendOnline ? "online" : "offline"}`}>
            Backend: {backendOnline ? "Online" : "Offline"}
          </p>
        </header>
        <main className={`app-main ${showTypeMap ? "three-pane" : ""}`}>
          <section className="pane pane-left">
            <div className="pane-header">
              <h2>Pseudo-code</h2>
            </div>
            <textarea
              className="code-input"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
            />
          </section>

          {showTypeMap && (
            <section className="pane pane-middle">
              <div className="pane-header">
                <h2>Type Map</h2>
              </div>
              <div className="type-map-content">
                {Object.keys(typeHints).length === 0 ? (
                  <div className="type-map-empty">
                    <p>No type mappings yet</p>
                    <p className="hint">
                      Convert your code to see variable types here
                    </p>
                  </div>
                ) : (
                  <div className="type-map-list">
                    {Object.entries(typeHints).map(([variable, type]) => (
                      <div key={variable} className="type-map-item">
                        <span className="var-name">{variable}</span>
                        <span className="arrow">→</span>
                        <span className="var-type">{type}</span>
                        <button
                          className="remove-type"
                          onClick={() => {
                            const newHints = { ...typeHints };
                            delete newHints[variable];
                            setTypeHints(newHints);
                          }}
                          title="Remove this type mapping"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
                <div className="type-map-actions">
                  <button
                    className="clear-types-btn"
                    onClick={() => setTypeHints({})}
                    disabled={Object.keys(typeHints).length === 0}
                  >
                    Clear All
                  </button>
                </div>
              </div>
            </section>
          )}

          <section className="pane pane-right">
            <div className="pane-header">
              <h2>C++ Output</h2>
            </div>
            <textarea
              className="code-output"
              value={cpp}
              readOnly
              spellCheck={false}
            />
          </section>
        </main>
        <footer className="app-footer">
          <button
            className="btn primary"
            onClick={handleConvert}
            disabled={loading}
          >
            {loading ? "Converting..." : "Convert to C++"}
          </button>
          <button
            className="btn secondary"
            onClick={handleCopy}
            disabled={!cpp}
          >
            Copy C++
          </button>
          <button
            className="btn secondary"
            onClick={() => setShowTypeMap(!showTypeMap)}
            title={showTypeMap ? "Hide Type Map" : "Show Type Map"}
          >
            {showTypeMap ? "Hide" : "Show"} Type Map
          </button>
          {pendingVar && (
            <div className="type-prompt">
              <span className="type-prompt-label">
                Select datatype for <strong>{pendingVar}</strong>:
              </span>
              <select
                className="type-select"
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
              >
                {VALID_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
              <button className="btn tertiary" onClick={handleConfirmType}>
                Confirm type
              </button>
            </div>
          )}
          {error && <div className="error-banner">{error}</div>}
        </footer>
      </div>
    </div>
  );
}

export default App;
