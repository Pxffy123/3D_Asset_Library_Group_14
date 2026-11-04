
import React from "react";
import styled from "styled-components";
import { Button } from "../styles";

function NavBar({ setUser }) {
  function handleLogoutClick() {
    localStorage.removeItem("token");
    setUser(null);
  }

  return (
    <Wrapper>
      <Logo>3D ASSET LIBRARY</Logo>
      <Button variant="outline" onClick={handleLogoutClick}>
        Logout
      </Button>
    </Wrapper>
  );
}

const Wrapper = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 6%;
  background: #10121b;
  border-bottom: 1px solid #303447;
`;

const Logo = styled.h1`
  font-size: 1.1rem;
  letter-spacing: 2px;
  color: #a99cff;
  margin: 0;
`;

export default NavBar;
