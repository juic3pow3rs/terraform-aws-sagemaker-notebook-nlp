import React, { useState, useEffect, useRef } from "react";
import {
  Box,
  TextField,
  IconButton,
  InputAdornment,
  Typography,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useTheme } from "@mui/material/styles";

const postData = async (url = '', data = {}) => {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return response.json(); // parse JSON response
};

function Chat() {
  const [review, setReview] = useState("");
  const [messages, setMessages] = useState([]);
  const endOfMessagesRef = useRef(null);
  const theme = useTheme();

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const addMessage = (text, type, loading = false, analysis = null) => {
    const messageId = Date.now();
    const newMessage = { id: messageId, text, type, loading, analysis };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    return messageId;
  };

  const updateMessage = (messageId, changes) => {
    setMessages((prevMessages) =>
      prevMessages.map((msg) =>
        msg.id === messageId ? { ...msg, ...changes } : msg
      )
    );
  };

  const simulateTyping = (messageId, analysisText) => {
    let currentText = "";
    let index = 0;
    const typeNextChar = () => {
      if (index < analysisText.length) {
        currentText += analysisText.charAt(index++);
        updateMessage(messageId, { text: currentText, loading: false }); // Ensure loading is false
        setTimeout(typeNextChar, 25); // Adjust typing speed as needed
      }
    };
    typeNextChar();
  };

const handleSubmit = async (e) => {
    e.preventDefault();
    const sentMessageId = addMessage(review, "sent");
    
    setReview("");

    try {
        const response = await postData('http://127.0.0.1:8080/predict-sentiment', { review });
        console.log('Response:', response);

        const { sentiment, topCritic, predictedScore } = response;
        const analysisText = `Sentiment: ${sentiment}\\nTop Critic: ${topCritic}\\nPredicted Score: ${predictedScore.toFixed(2)} / 5\\n${selectEmoji(
            predictedScore
        )}`;

        // Add a placeholder for analysis without loading state, then start typing
        const analysisMessageId = addMessage("", "analysis");
        simulateTyping(analysisMessageId, analysisText);
    } catch (error) {
        console.error('Error:', error);
    }
};

  const selectEmoji = (score) => {
    if (score >= 3.33) {
      return "\\(^▽^)/";
    } else if (score > 1.66) {
      return "¯\\_(ツ)_/¯";
    } else {
      return "(︶︹︺)";
    }
  };

  // Handling Enter key press for sending message
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "90%",
        width: "80%",
        justifyContent: "space-between",
        background: "rgba(255, 255, 255, 0.05)",
        "border-radius": "16px",
        "box-shadow": " 0 4px 30px rgba(0, 0, 0, 0.1)",
        "backdrop-filter": "blur(11.9px)",
        "-webkit-backdrop-filter": "blur(11.9px)",
        border: "1px solid rgba(255, 255, 255, 0.51)",
        padding: "30px",
      }}
    >
      <Box sx={{ overflowY: "auto", flexGrow: 1, padding: "10px" }}>
        {messages.map((msg) => (
          <Box
            key={msg.id}
            sx={{
              display: "flex",
              justifyContent:
                msg.type === "analysis" ? "flex-start" : "flex-end",
              marginBottom: 1,
            }}
          >
            <Typography
              variant="body1"
              component="div"
              sx={{
                background: msg.type === "analysis" ? "#202c33" : "#005c4b",
                display: "inline-block",
                padding: 1,
                borderRadius: "10px",
                maxWidth: "80%",
                color: "white",
                position: "relative",
                fontSize: "1.55rem",
              }}
            >
              {msg.text.split("\\n").map((m) => (
                <div>
                  {m}
                  <br />
                </div>
              ))}
            </Typography>
          </Box>
        ))}
        <div ref={endOfMessagesRef} />
      </Box>

      {/* Chat input area */}
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          alignItems: "center",
          padding: "10px",
          borderTop: `1px solid ${theme.palette.grey[300]}`,
        }}
      >
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={review}
          onChange={(e) => setReview(e.target.value)}
          onKeyPress={handleKeyPress}
          variant="outlined"
          label="Write your movie review..."
          sx={{
            mr: 1,
            background: theme.palette.background.paper,
            borderRadius: "15px",
          }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton type="submit" sx={{ p: "10px" }} aria-label="send">
                  <SendIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Box>
    </Box>
  );
}

export default Chat;
