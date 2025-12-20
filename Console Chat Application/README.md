# 💬 Java Console-Based Chat Application








# # 📌 Overview

The Java Console-Based Chat Application is a real-time, multi-user messaging system built using core Java networking and multithreading concepts.
It allows multiple clients to connect to a central server and exchange messages instantly through the command-line interface.

This project demonstrates how low-level networking, concurrency, and object-oriented design work together to form a functional communication system—similar in concept to real-world chat servers.

## ✨ Key Highlights

🔹 Real-time text communication

🔹 Multiple clients supported simultaneously

🔹 Centralized server architecture

🔹 Uses Java Sockets and Streams

🔹 Fully console-based (no GUI dependency)

🔹 Clean, modular, object-oriented design

🔹 Beginner-friendly yet industry-relevant

## 🛠️ Technologies & Concepts Used
Category	Technologies
Language	Java
Networking	Socket, ServerSocket
I/O	BufferedReader, InputStreamReader, PrintWriter
Concurrency	Multithreading (Thread class)
Architecture	Client–Server Model
Platform	Cross-platform (Windows / Linux / macOS)
### 🧩 Project Structure
📦 Java-Console-Chat-App
 ┣ 📜 Server.java
 ┣ 📜 Client.java
 ┣ 📜 ClientHandler.java
 ┗ 📜 README.md

## 🔹 File Responsibilities

Server.java → Starts the server and listens for incoming client connections

ClientHandler.java → Handles communication for each connected client using threads

Client.java → Connects to the server and enables message sending/receiving

## ⚙️ How It Works (Architecture)

The Server starts and listens on a specific port

Each Client connects using a socket

For every client, a new thread is created

Messages are transmitted using I/O streams

The server relays messages between connected clients

This ensures non-blocking, real-time communication.

## 🚀 How to Run the Project
### ✅ Prerequisites

Java JDK 8 or above

Command Prompt / Terminal

Basic knowledge of running Java programs

▶️ Steps to Execute
1️⃣ Compile all files
javac Server.java Client.java ClientHandler.java

2️⃣ Start the server (Terminal 1)
java Server

3️⃣ Start clients (Terminal 2, 3, …)
java Client


You can open multiple terminals to simulate multiple users.

## 📸 Output Screenshots
🔹 Server Running
🔹 Multiple Clients Chatting
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/a0159fc4-1367-43da-99bb-867297d5f074" />
<img width="1270" height="552" alt="image" src="https://github.com/user-attachments/assets/1cea5ff7-0eba-49a8-99bd-a308f70733dc" />
<img width="1360" height="768" alt="image" src="https://github.com/user-attachments/assets/c69fd60e-e83f-44d2-b594-cdd2beadbb54" />




## 🔐 Features in Detail

✔️ Handles multiple users concurrently

✔️ Continuous message listening (real-time)

✔️ Graceful handling of client disconnections

✔️ Efficient stream-based communication

✔️ Lightweight & fast execution

## 🧠 Learning Outcomes

Through this project, you gain hands-on experience with:

Java networking fundamentals

Client-server communication

Multithreading and concurrency

Console-based application design

Object-Oriented Programming principles

Real-world backend communication logic

## 📈 Future Enhancements

🔸 Private (one-to-one) messaging

🔸 User authentication (username/password)

🔸 Message timestamps

🔸 Chat history logging

🔸 GUI version using JavaFX / Swing

🔸 Encryption for secure communication

## 👨‍💻 Author

Aditya Gupta
🎓 B.Tech – Computer Science & Engineering
💻 Java | DSA | Web Development

Built with dedication to strengthen core Java & networking concepts.

##  ⭐ Support

If you found this project useful:

## ⭐ Star the repository

🍴 Fork it

🧠 Use it to learn & improve
