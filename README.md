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
| **Backend / Data Source** | Google Sheets (owned by Pasar Padel) |
| **Environment Variables** | Stored securely in `.env` on Render.com |

All application logic and authentication details for connecting to Google Sheets are handled via environment variables.  
This ensures sensitive credentials are **never stored directly in the repository**.

---

## 🗂️ Data Model

Data is stored in **Google Sheets**, as per Pasar Padel’s request.  
The sheet structure is **tabular** and **non-normalized**, designed for ease of access by store staff rather than for database optimization.

---

## ⚙️ Setup & Deployment

> 🧠 Note: To successfully deploy or run this project, you will need access to the necessary credentials and Google Sheets configuration owned by **Pasar Padel**.

### Prerequisites
- Access to the Pasar Padel Google Sheet
- `.env` file containing:
  - Google Sheets API credentials
  - Spreadsheet ID
  - Any additional environment variables required by the app
