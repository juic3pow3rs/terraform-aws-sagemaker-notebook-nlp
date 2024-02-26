import React from "react";
import { Card, Typography, CssBaseline } from "@mui/material";
import Chat from "./Chat"; // Assuming Chat is in the same directory

function App() {
  return (
    <div className="App">
      <CssBaseline /> {/* Ensures consistent styling across browsers */}
      <Card
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          width: "100vw",
          flexDirection: "column",
          background: "#171717", // Adds a vibrant gradient background
          overflow: "hidden",
          padding: "20px", // Provides spacing inside the card
        }}
      >
        <Typography
          variant="h3"
          component="h1"
          sx={{
            color: "#fff", // Ensures text stands out against the background
            textShadow: "0px 4px 4px rgba(0, 0, 0, 0.25)", // Adds a subtle shadow for depth
            marginBottom: "20px", // Adds space below the title
          }}
        >
          Movie Review Sentiment Analysis
        </Typography>
        <Chat />
      </Card>
    </div>
  );
}

export default App;
