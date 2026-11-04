
import React, { useEffect, useState } from "react";

function AssetDashboard({ user, token }) {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    name: "",
    description: "",
    category: "character",
    format: "BLEND",
  });

  const [editingId, setEditingId] = useState(null);

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };

  async function loadAssets() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch("/assets?page=1&per_page=100", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Could not load assets.");
      }

      setAssets(data.items || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAssets();
  }, [token]);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const url = editingId
        ? `/assets/${editingId}`
        : "/assets";

      const response = await fetch(url, {
        method: editingId ? "PATCH" : "POST",
        headers,
        body: JSON.stringify(form),
      });

      const data = response.status === 204 ? {} : await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Could not save asset.");
      }

      setMessage(editingId ? "Asset updated successfully!" : "Asset created successfully!");
      setForm({
        name: "",
        description: "",
        category: "character",
        format: "BLEND",
      });
      setEditingId(null);
      await loadAssets();
    } catch (err) {
      setError(err.message);
    }
  }

  function startEditing(asset) {
    setEditingId(asset.id);
    setForm({
      name: asset.name,
      description: asset.description,
      category: asset.category,
      format: asset.format,
    });
    setMessage("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function deleteAsset(id) {
    if (!window.confirm("Are you sure you want to delete this asset?")) {
      return;
    }

    try {
      setError("");
      setMessage("");

      const response = await fetch(`/assets/${id}`, {
        method: "DELETE",
        headers,
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Could not delete asset.");
      }

      setMessage("Asset deleted successfully!");
      await loadAssets();
    } catch (err) {
      setError(err.message);
    }
  }

  function cancelEditing() {
    setEditingId(null);
    setForm({
      name: "",
      description: "",
      category: "character",
      format: "BLEND",
    });
  }

  const styles = {
    page: {
      minHeight: "100vh",
      background: "#10121b",
      color: "#f4f4f8",
      padding: "35px 6%",
      fontFamily: "Arial, sans-serif",
    },
    heading: {
      fontSize: "32px",
      marginBottom: "8px",
    },
    muted: {
      color: "#a5a8bb",
    },
    panel: {
      background: "#1b1e2b",
      padding: "24px",
      borderRadius: "12px",
      margin: "25px 0",
      border: "1px solid #303447",
    },
    input: {
      width: "100%",
      padding: "12px",
      margin: "8px 0 16px",
      borderRadius: "6px",
      border: "1px solid #41465c",
      background: "#111522",
      color: "white",
      boxSizing: "border-box",
    },
    button: {
      padding: "11px 18px",
      border: "none",
      borderRadius: "6px",
      background: "#7565e8",
      color: "white",
      cursor: "pointer",
      fontWeight: "bold",
      marginRight: "8px",
    },
    grid: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(230px, 1fr))",
      gap: "18px",
    },
    card: {
      background: "#1b1e2b",
      border: "1px solid #303447",
      padding: "20px",
      borderRadius: "12px",
    },
    tag: {
      display: "inline-block",
      background: "#302b55",
      color: "#c8c0ff",
      padding: "5px 9px",
      borderRadius: "20px",
      fontSize: "12px",
      marginRight: "6px",
      marginTop: "8px",
    },
  };

  return (
    <div style={styles.page}>
      <header>
        <p style={{ color: "#a99cff", fontWeight: "bold", letterSpacing: "2px" }}>
          3D ASSET LIBRARY
        </p>
        <h1 style={styles.heading}>Your creative workspace.</h1>
        <p style={styles.muted}>
          Welcome, {user.username}. Manage your 3D assets in one place.
        </p>
      </header>

      <section style={styles.panel}>
        <h2>{editingId ? "Edit Asset" : "Add a New Asset"}</h2>

        <form onSubmit={handleSubmit}>
          <label>Asset Name</label>
          <input
            style={styles.input}
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="e.g. Fantasy Warrior"
            required
          />

          <label>Description</label>
          <textarea
            style={{ ...styles.input, minHeight: "85px" }}
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="Describe your asset..."
            required
          />

          <label>Category</label>
          <select
            style={styles.input}
            name="category"
            value={form.category}
            onChange={handleChange}
          >
            <option value="character">Character</option>
            <option value="environment">Environment</option>
            <option value="material">Material</option>
            <option value="simulation">Simulation</option>
          </select>

          <label>File Format</label>
          <select
            style={styles.input}
            name="format"
            value={form.format}
            onChange={handleChange}
          >
            <option value="BLEND">BLEND</option>
            <option value="FBX">FBX</option>
            <option value="OBJ">OBJ</option>
            <option value="EXR">EXR</option>
          </select>

          <button style={styles.button} type="submit">
            {editingId ? "Save Changes" : "Add Asset"}
          </button>

          {editingId && (
            <button
              style={{ ...styles.button, background: "#555b70" }}
              type="button"
              onClick={cancelEditing}
            >
              Cancel
            </button>
          )}
        </form>

        {message && <p style={{ color: "#76dfa4" }}>{message}</p>}
        {error && <p style={{ color: "#ff8585" }}>{error}</p>}
      </section>

      <section>
        <h2>Your Assets ({assets.length})</h2>

        {loading && <p style={styles.muted}>Loading assets...</p>}

        {!loading && assets.length === 0 && (
          <p style={styles.muted}>No assets yet. Add your first one above!</p>
        )}

        <div style={styles.grid}>
          {assets.map((asset) => (
            <article key={asset.id} style={styles.card}>
              <h3>{asset.name}</h3>
              <p style={styles.muted}>{asset.description}</p>

              <span style={styles.tag}>{asset.category}</span>
              <span style={styles.tag}>{asset.format}</span>

              <div style={{ marginTop: "20px" }}>
                <button
                  style={styles.button}
                  onClick={() => startEditing(asset)}
                >
                  Edit
                </button>

                <button
                  style={{ ...styles.button, background: "#a83e55" }}
                  onClick={() => deleteAsset(asset.id)}
                >
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

export default AssetDashboard;
