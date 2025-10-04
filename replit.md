# Consultas Online - Real-time Video Consultation System

## Overview
This project, branded as "MedConnect," is a real-time video consultation platform built with Flask and Socket.IO, primarily for the medical field. It supports three user types (Admin, Doctor, Patient) with secure authentication, patient evolution tracking, and dedicated consultation rooms. The platform aims to provide a comprehensive, intuitive, and efficient online consultation system for healthcare professionals to manage patients, conduct video consultations, and maintain medical records.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### UI/UX Decisions
The application features a modern UX/DX design with a consistent blue/cyan medical theme, gradient backgrounds, and glassmorphism effects. It utilizes the Inter font family from Google Fonts and is fully responsive across desktop, tablet, and mobile devices. Dashboards employ card-based interfaces with hover effects and animated statistics. Video call layouts are role-based, optimizing prominent display for the main participant. All pages include a consistent branding footer.

### Technical Implementations
The backend uses **Flask** and **Flask-SocketIO** for real-time bidirectional communication, essential for **WebRTC** signaling. **WebRTC** facilitates peer-to-peer video/audio streaming, leveraging Google's public STUN server. Authentication uses Flask sessions with **werkzeug** for password hashing and custom role-based access control. Consultation room codes are randomly generated.

### Feature Specifications
-   **User Management**: Admins manage doctors and patients; doctors can register their own patients.
-   **Consultation Rooms**: Unique, dedicated rooms for doctor-patient consultations.
-   **Medical Evolution Tracking**: Doctors record patient notes, diagnoses, and prescriptions.
-   **Billing System**: Admins configure fees. The system automatically creates billing records for finalized evolutions or video calls, calculating revenue for doctors and admins. Both roles have dashboards for billing history and reports.
-   **Monthly Closings System**: A comprehensive payment management system allowing admins to create, confirm, and track monthly payments for doctors, with a two-step verification process (Admin confirms payment → Doctor confirms receipt) and a complete audit trail.
-   **PIX Payment Integration**: Doctors can register their PIX key in their profile page. When admins generate monthly closing reports, the system exports an Excel spreadsheet containing doctor names, net payment amounts, and their PIX keys for easy payment processing.
-   **Excel Export for Payments**: Admins can export professionally formatted Excel spreadsheets with payment details including doctor information, consultation counts, gross/net amounts, PIX keys, and payment status.
-   **Database Reset**: Admin-only feature to reset the entire database while preserving the admin account, requiring confirmation.
-   **Role-based Dashboards**: Tailored dashboards for Admin (user management, billing config, revenue, closings, database reset), Doctor (patient management, rooms, evolutions, billing history, payments), and Patient (access rooms, medical history).
-   **Real-time Presence**: Visual status and notifications for participant connection states in video calls.
-   **Consultation Finalization**: Doctors can finalize consultations, deactivating rooms and prompting new room creation.
-   **Patient Details View**: Dedicated pages for doctors to view patient information and medical history.
-   **Automatic Consultation Registration**: Each video call registers a billable consultation, linked to doctor's rates.
-   **Profile Photo System**: Secure upload and display of user profile photos with file validation, size limits, and graceful fallbacks to user initials across various list views and dashboards.

### System Design Choices
-   **Backend Framework**: Flask with Flask-SocketIO for lightweight, real-time WebSocket support.
-   **Database**: **SQLite** for serverless, embedded persistent storage. The schema includes tables for users, doctors, patients, consultation rooms, medical evolutions, billing configurations, consultation records, and monthly closings.
-   **Real-time Signaling**: Socket.IO WebSockets for reliable exchange of WebRTC session descriptions and ICE candidates using room-based communication.

## External Dependencies
-   **Flask**: Web framework for the backend.
-   **Flask-SocketIO**: Enables WebSocket communication.
-   **python-socketio**: Python implementation of the Socket.IO protocol.
-   **python-engineio**: Engine.IO server implementation for real-time bidirectional communication.
-   **gunicorn**: WSGI HTTP Server for production deployments.
-   **openpyxl**: Library for creating and formatting Excel spreadsheets (used for payment reports).
-   **Socket.IO Client**: CDN-hosted client-side library for WebSocket communication.
-   **Google STUN Server**: Used for NAT traversal in WebRTC (`stun:stun.l.google.com:19302`).
-   **SQLite**: Embedded database for all persistent data storage.
-   **Environment Variables**: `SESSION_SECRET` (Flask secret key), `ADMIN_PASSWORD` (optional admin password).

## Recent Changes (October 2025)
-   **CRITICAL FIX:** Resolved WebSocket worker timeout issues on Render
    - Increased Gunicorn timeout from 120s to 300s (5 minutes) for stable long video calls
    - Ensured consistent `gthread` worker configuration across all files (Procfile, start.sh, gunicorn_config.py)
    - This fixes the "WORKER TIMEOUT" and slow loading issues when doctors open video calls
    - Note: Eventlet is incompatible with Python 3.13, so using threading mode with gthread worker
-   **WebRTC Performance Optimizations (October 4, 2025)** - Significant lag reduction
    - Configured video quality constraints: 640x480@24fps ideal, max 1280x720@30fps
    - Implemented bitrate limiting: 500kbps max for stable connections, auto-reduces to 300kbps on poor networks
    - Added automatic network quality monitoring (checks every 3 seconds)
    - Implemented adaptive quality adjustment based on packet loss and jitter metrics
    - Enhanced audio with echo cancellation, noise suppression, and auto gain control
    - Added connection state monitoring with user notifications
    - Optimized WebRTC config: max-bundle policy, require RTCP mux for reduced overhead
-   Added `chave_pix` field to the `medicos` table for storing doctor PIX payment keys.
-   Implemented PIX key management in doctor profile page with update functionality.
-   Created Excel export feature for monthly payment closings with formatted spreadsheets including PIX information.
-   Enhanced admin payment workflow with professional Excel reports for easier payment processing.

## Performance Optimizations for Render (October 2025)
-   **System Config Cache**: 5-minute in-memory cache to reduce repeated database queries for system configurations
-   **SQLite Indexes**: Added 15+ strategic indexes on frequently queried columns (user_id, medico_id, paciente_id, dates, etc.)
-   **SQLite Performance PRAGMAs**: 
    - WAL mode for better concurrent read/write performance
    - NORMAL synchronous mode for faster writes with minimal risk
    - 64MB cache size, memory-based temp storage
    - 128MB memory-mapped I/O
-   **Socket.IO Tuning**: 
    - Configured ping_timeout=60s and ping_interval=25s for stable WebSocket connections
    - Client configured with WebSocket-first transport, automatic reconnection
    - Multiple STUN servers for improved NAT traversal
-   **WebRTC Video Call Optimizations**:
    - Smart video quality limits (640x480 ideal, max 1280x720) prevent bandwidth saturation
    - Bitrate capping at 500kbps with automatic reduction to 300kbps on poor connections
    - Real-time network monitoring detects packet loss and jitter issues
    - Adaptive quality scaling automatically adjusts resolution when connection degrades
    - Enhanced audio processing reduces echo, noise, and normalizes volume
    - Connection state notifications keep users informed of network status
-   **Gunicorn Configuration**: 
    - **Single worker (w=1) with 100 threads**
    - Worker class: gthread (multi-threaded, Python 3.13 compatible)
    - Threading mode with 100 threads provides stable WebSocket support
    - Timeout: 300s (5 minutes) for stable long video calls without interruption
-   **Production Scripts**: Created `start.sh` with optimized Gunicorn command

### Render Deployment

**IMPORTANTE:** Configure manualmente no painel do Render para garantir que o worker gthread seja usado.

**Build Command:** `pip install -r requirements.txt`

**Start Command (CONFIGURAR MANUALMENTE NO PAINEL DO RENDER):** 
```
gunicorn -c gunicorn_config.py app:app
```

**⚠️ ATENÇÃO:** NÃO deixe o Render detectar automaticamente! Ele pode usar o worker sync errado. Você DEVE configurar o Start Command manualmente no painel do Render em Settings → Build & Deploy.

**Environment Variables:**
- `SESSION_SECRET` - Required: Random secure key for Flask sessions
- `PORT` - Auto-provided by Render

**Python Version:**
- Works with Python 3.11+ and 3.13+ (gthread threading mode is fully compatible)
- No special Python version restrictions needed

**Critical Configuration:**
- ⚠️ **MUST use `gthread` worker class** - The default `sync` worker will cause WebSocket timeouts
- Threading mode with 100 threads provides stable WebSocket support
- Single worker is sufficient for Socket.IO
- Timeout set to 300s (5 minutes) to handle long video calls without interruption
- **CONFIGURE MANUALMENTE:** Não confie na detecção automática do Render - sempre configure o Start Command manualmente

**Como Configurar no Render:**
1. Acesse o Dashboard do seu serviço no Render
2. Vá em **Settings** → **Build & Deploy**
3. Em **Start Command**, cole: `gunicorn -c gunicorn_config.py app:app`
4. Clique em **Save Changes**
5. Faça um **Manual Deploy** para aplicar as mudanças

**Important Notes:**
- Render Free tier has 5-minute idle timeout on WebSocket connections
- For production video calls longer than 5 minutes, upgrade to paid plan