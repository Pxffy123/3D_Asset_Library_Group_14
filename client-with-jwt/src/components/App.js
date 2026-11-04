
import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import AssetDashboard from "./AssetDashboard";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) return;

    fetch("/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          localStorage.removeItem("token");
          return null;
        }
        return response.json();
      })
      .then((data) => {
        if (data) setUser(data);
      })
      .catch(() => {
        localStorage.removeItem("token");
      });
  }, []);

  const onLogin = (token, user) => {
    localStorage.setItem("token", token);
    setUser(user);
  };

  if (!user) {
    return <Login onLogin={onLogin} />;
  }

  return (
    <>
      <NavBar setUser={setUser} />
      <AssetDashboard
        user={user}
        token={localStorage.getItem("token")}
      />
    </>
  );
}

export default App;
