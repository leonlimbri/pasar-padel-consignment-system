# 🏸 Pasar Padel Consignment Tracker

A lightweight web application built for **Pasar Padel** to help manage and track **store consignments**, **item inventory**, and **revenue progress**.

---

## 🚀 Overview

The **Pasar Padel Consignment Tracker** is a simple CRUD (Create, Read, Update, Delete) web app that allows the store to:

- Track all items sent on consignment  
- Monitor sales and revenue progress  
- View summarized reports of consignment performance  

The app provides a minimal, practical interface focused on usability and speed for the store’s daily operations.

---

## 🧩 System Architecture

| Component | Description |
|------------|--------------|
| **Frontend / Web App** | Hosted on [Render.com](https://render.com) |
| **Backend / Data Source** | SQLite3 (owned by Pasar Padel) |
| **Environment Variables** | Stored securely in `.env` on Render.com |

All application logic and authentication details are handled via environment variables.  
This ensures sensitive credentials are **never stored directly in the repository**.

---

## 🗂️ Data Model

Data is stored in **Sqlite Database**, to improve the get/set functionalities.

---

## ⚙️ Setup & Deployment

> 🧠 Note: To successfully deploy or run this project, you will need access to the necessary credentials and Google Sheets configuration owned by **Pasar Padel**.

### Prerequisites
- Access to the Pasar Padel Google Sheet
- `.env` file containing:
  - Folder path to the sqlite database
  - Any additional environment variables required by the app