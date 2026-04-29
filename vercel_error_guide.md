# 🚩 Vercel Error Troubleshooting Guide

This document summarizes common Vercel deployment errors and their solutions. Use this as a reference if you encounter issues during the deployment of the **Multi-Feature Face Processing System**.

---

## 🏗️ Build & Structure Errors

### 1. Missing Public Directory
*   **Cause**: The build output directory is missing or empty.
*   **Solution**: Ensure the output directory is correctly specified in project settings or that your build command (e.g., `streamlit build`) generates files in the expected location.

### 2. Unmatched Function Pattern
*   **Cause**: The `functions` property in `vercel.json` doesn't match files in the `api` directory.
*   **Solution**: Ensure your glob patterns start with `api/` (e.g., `"api/**/*.py"`).

### 3. Missing Build Script
*   **Cause**: `package.json` is present but lacks a `build` script.
*   **Solution**: Add a `"build": "[command]"` script to your `package.json`.

---

## 🔑 Configuration & Routing

### 1. Invalid Route Source Pattern
*   **Cause**: Using RegExp syntax instead of `path-to-regexp` syntax in `vercel.json`.
*   **Solution**: Wrap negative lookaheads in groups: `"/feedback/((?!general).*)"`.

### 2. Conflicting Configuration Files
*   **Cause**: Having both `vercel.json` and `now.json` (or `.vercelignore` and `.nowignore`).
*   **Solution**: Delete the older `now.*` files.

### 3. Conflicting Functions and Builds
*   **Cause**: Using both `functions` and `builds` properties in `vercel.json`.
*   **Solution**: It is recommended to use the `functions` property for more features.

---

## 📦 Dependency & Size Issues

### 1. Failed to Install Builder Dependencies
*   **Cause**: `npm install` errors while installing builders defined in `vercel.json`.
*   **Solution**: Check internet connection and ensure the builder name/version is correct.

### 2. Globally Installed Analytics/Speed-Insights
*   **Cause**: Packages are available globally but not listed in `package.json`.
*   **Solution**: Add `@vercel/speed-insights` or `@vercel/analytics` to your `package.json` dependencies.

---

## 🔒 Access & Permissions

### 1. Team Access Required
*   **Cause**: Commit author doesn't have a Vercel account or team membership.
*   **Solution**: Link your Git provider to a Vercel account and ensure you are a member of the deploying team.

### 2. Blocked Scopes
*   **Cause**: Violation of fair use guidelines or Terms of Service.
*   **Solution**: Reach out to `registration@vercel.com`.

---

## 🌐 Domain & SSL

### 1. Domain Verification Failed
*   **Cause**: Domain is not pointed to Vercel nameservers or DNS records.
*   **Solution**: Run `vercel domains inspect <domain>` to check requirements.

### 2. SSL Certificate Deletion Denied
*   **Cause**: Managed SSL certificates cannot be manually deleted.
*   **Solution**: Only custom uploaded certificates on Enterprise plans can be manually deleted.

---

## 🛠️ Local Development

### 1. Command Not Found in `vercel dev`
*   **Cause**: A required binary (like `go` or `python`) is not installed locally.
*   **Solution**: Install the missing language/tool on your operating system.

### 2. Recursive Invocation
*   **Cause**: Your build command invokes `vercel build` itself.
*   **Solution**: Change the build command to the framework-specific build command (e.g., `npm run build`).
