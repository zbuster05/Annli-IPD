import React from "react";

const IPD_RULES = "https://docs.google.com/document/d/1QBg-bVN7hnfhVqC6DOtP7xCliUXCygvuav8kEVUnOzc/edit?usp=sharing"

const Header = () => {
    return(
        <>
        <h1>IPD Online</h1>
        <p>hi :)</p>
        <p><a href={IPD_RULES} target="_blank" rel="noreferrer">Review IPD rules</a></p>
        </>
    )
}

export default Header;