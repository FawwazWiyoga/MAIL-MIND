# PRODUCT REQUIREMENTS DOCUMENT (PRD)
# MailMind AI

**Version:** 1.0  
**Status:** Initial Draft  
**Date:** 23 November 2026  
**Product Type:** Open-Source, Multi-User AI Email Workspace  
**Platforms:** Web Application & Desktop Application  
**Primary Language:** English (initial interface), with extensible localization  
**Repository:** https://github.com/FawwazWiyoga/MAIL-MIND.git

---

# 1. Executive Summary

## 1.1 Product Overview

MailMind AI adalah aplikasi manajemen email berbasis Artificial Intelligence (AI) yang dirancang untuk membantu pengguna mengelola, memahami, mencari, dan menindaklanjuti email secara lebih efisien.

Aplikasi ini mengintegrasikan layanan email dengan teknologi Large Language Models (LLM), Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), dan semantic search.

MailMind AI tidak hanya berfungsi sebagai email client, tetapi juga sebagai intelligent email workspace yang mampu memahami konteks komunikasi dan membantu pengguna mengambil tindakan berdasarkan isi email.

Aplikasi dikembangkan dalam dua platform:

- **Web Application:** Dapat diakses melalui browser.
- **Desktop Application:** Aplikasi desktop berbasis Tauri 2 dengan penggunaan kembali frontend web.

MailMind AI dirancang sebagai proyek open-source yang mendukung banyak pengguna dengan isolasi data dan keamanan pada tingkat akun.

## 1.2 Problem Statement

Pengelolaan email secara konvensional memiliki beberapa permasalahan:

1. Pengguna membutuhkan waktu untuk membaca email dalam jumlah besar.
2. Email penting dapat tertimbun oleh pesan yang kurang relevan.
3. Informasi tugas, tenggat waktu, dan tindak lanjut tersebar dalam berbagai percakapan.
4. Pencarian berbasis kata kunci tidak selalu dapat memahami maksud pengguna.
5. Pengguna harus membaca ulang percakapan panjang untuk menemukan informasi tertentu.
6. Pengelolaan email belum sepenuhnya memanfaatkan AI untuk memahami konteks komunikasi.

MailMind AI bertujuan mengatasi permasalahan tersebut melalui sistem pengelolaan email yang terintegrasi dengan AI.

## 1.3 Product Vision

Menjadi intelligent email workspace open-source yang membantu pengguna mengubah email dari sekadar media komunikasi menjadi sumber informasi dan tindakan yang terorganisasi.

---

# 2. Product Goals and Non-Goals

## 2.1 Product Goals

Tujuan utama pengembangan MailMind AI:

| ID | Goal | Description |
|---|---|---|
| G-01 | Email Management | Mengintegrasikan dan mengelola email dalam satu workspace |
| G-02 | AI Summarization | Membuat ringkasan email dan percakapan |
| G-03 | Smart Categorization | Mengelompokkan email secara otomatis |
| G-04 | Priority Detection | Mengidentifikasi email berdasarkan tingkat kepentingan |
| G-05 | Action Extraction | Mengidentifikasi tugas, deadline, dan tindak lanjut |
| G-06 | Intelligent Search | Mendukung pencarian berbasis semantic search dan bahasa alami |
| G-07 | AI Assistant | Menyediakan interaksi percakapan berdasarkan konteks email |
| G-08 | Multi-Platform | Mendukung web dan desktop |
| G-09 | Open Source | Menyediakan kode sumber yang dapat dikembangkan komunitas |
| G-10 | Security | Menjamin isolasi data dan perlindungan informasi pengguna |

## 2.2 Non-Goals

Hal-hal berikut tidak menjadi prioritas pada versi awal:

- Mengembangkan layanan email server sendiri.
- Menggantikan infrastruktur Gmail atau Outlook.
- Mengembangkan model LLM dari awal.
- Mengirim atau menghapus email secara otomatis tanpa persetujuan pengguna.
- Mendukung seluruh penyedia email sejak versi pertama.
- Mengimplementasikan microservices pada tahap awal.
- Mengembangkan aplikasi mobile native pada MVP.
- Menjamin seluruh layanan AI tersedia secara gratis tanpa batas.

---

# 3. Target Users

## 3.1 User Personas

### Persona A — Student

Kebutuhan:
- Mengelola email akademik.
- Menemukan informasi tugas dan jadwal.
- Mendapatkan ringkasan pengumuman.
- Mengidentifikasi deadline.

### Persona B — Professional

Kebutuhan:
- Mengelola komunikasi pekerjaan.
- Menentukan email prioritas.
- Membuat draft balasan.
- Mengidentifikasi pekerjaan yang membutuhkan tindak lanjut.

### Persona C — Business User

Kebutuhan:
- Mengelola volume email yang tinggi.
- Memahami percakapan panjang.
- Mengelompokkan komunikasi berdasarkan konteks.
- Mengidentifikasi informasi dan keputusan penting.

### Persona D — Developer / Open-Source Contributor

Kebutuhan:
- Mengakses kode sumber.
- Mengembangkan integrasi baru.
- Menambahkan AI provider.
- Mengembangkan fitur dan memperbaiki bug.

## 3.2 User Roles

| Role | Permissions |
|---|---|
| Guest | Mengakses halaman publik |
| User | Mengelola akun, email, dan pengaturan pribadi |
| Admin | Mengelola konfigurasi sistem dan administrasi platform |
| Developer | Mengembangkan proyek melalui repository |

Admin platform tidak boleh memperoleh akses bebas terhadap isi email pribadi pengguna.

---

# 4. Product Scope

## 4.1 Platform

### Web Application

Teknologi:
- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

Fungsi:
- Dashboard email.
- Inbox dan email management.
- AI assistant.
- Search.
- Settings.
- Account management.

### Desktop Application

Teknologi:
- Tauri 2.
- Reuse frontend web.
- Integrasi kemampuan desktop secara bertahap.

Fungsi:
- Menjalankan MailMind AI sebagai aplikasi desktop.
- Mendukung notifikasi desktop.
- Mendukung pengalaman penggunaan tanpa membuka browser.
- Menggunakan backend dan API yang sama dengan web.

## 4.2 Initial Email Provider

| Provider | Priority | Integration |
|---|---|---|
| Gmail | High | Gmail API + Google OAuth |
| Outlook | Medium | Microsoft Graph API |
| IMAP/SMTP | Future | Provider abstraction |

Integrasi Gmail menjadi prioritas pertama.

---

# 5. Functional Requirements

## 5.1 Authentication and Account Management

**FR-001 — User Registration**

Sistem menyediakan registrasi akun pengguna.

**FR-002 — User Login**

Sistem menyediakan autentikasi pengguna yang aman.

**FR-003 — Session Management**

Sistem mengelola sesi pengguna dan menyediakan mekanisme logout.

**FR-004 — OAuth Integration**

Pengguna dapat menghubungkan akun Gmail melalui Google OAuth.

**FR-005 — Account Disconnection**

Pengguna dapat memutus koneksi akun email.

**FR-006 — Account Deletion**

Pengguna dapat menghapus akun dan meminta penghapusan data yang terkait sesuai kebijakan retensi.

## 5.2 Email Management

**FR-007 — Inbox**

Sistem menampilkan daftar email yang tersinkronisasi.

**FR-008 — Email Detail**

Sistem menampilkan informasi email, termasuk:

- Sender.
- Recipient.
- Subject.
- Timestamp.
- Email body.
- Attachments metadata.
- Thread information.

**FR-009 — Email Synchronization**

Sistem mengambil dan memperbarui data email melalui provider API.

**FR-010 — Email Filtering**

Pengguna dapat menyaring email berdasarkan:

- Sender.
- Date.
- Subject.
- Labels.
- Read/unread status.
- Priority.

**FR-011 — Email Pagination**

Sistem mendukung pagination atau incremental loading untuk menghindari pemuatan seluruh email sekaligus.

## 5.3 AI Email Summarization

**FR-012 — Email Summary**

AI menghasilkan ringkasan isi email.

**FR-013 — Thread Summary**

AI menghasilkan ringkasan dari percakapan email yang terdiri dari beberapa pesan.

**FR-014 — Key Information Extraction**

AI dapat mengidentifikasi:

- Informasi utama.
- Keputusan.
- Permintaan.
- Instruksi.
- Tanggal penting.
- Informasi tambahan yang relevan.

Ringkasan harus tetap dapat ditelusuri ke email sumber.

## 5.4 Smart Categorization

**FR-015 — Automatic Categorization**

AI mengklasifikasikan email berdasarkan kategori yang ditentukan sistem.

Kategori awal:

- Work.
- Personal.
- Academic.
- Finance.
- Promotion.
- Notification.
- Meeting.
- Important.
- Other.

**FR-016 — User Correction**

Pengguna dapat mengubah kategori email.

**FR-017 — Classification Confidence**

Sistem dapat menyimpan tingkat keyakinan klasifikasi jika model atau provider menyediakannya.

## 5.5 Priority Detection

**FR-018 — Priority Analysis**

AI mengidentifikasi tingkat prioritas email.

Klasifikasi awal:

| Priority | Meaning |
|---|---|
| Critical | Membutuhkan perhatian segera |
| High | Penting dan perlu ditindaklanjuti |
| Medium | Relevan tetapi tidak mendesak |
| Low | Tidak membutuhkan tindakan segera |

Penentuan prioritas harus berdasarkan konteks, bukan hanya kata-kata tertentu.

Pengguna tetap dapat mengubah prioritas secara manual.

## 5.6 Action Item Extraction

**FR-019 — Task Extraction**

AI mengidentifikasi tugas atau tindakan yang diminta dalam email.

**FR-020 — Deadline Detection**

AI mengidentifikasi tanggal dan tenggat waktu yang disebutkan.

**FR-021 — Action Item Management**

Pengguna dapat melihat dan mengelola daftar tindakan yang dihasilkan AI.

Setiap action item memiliki:

- Description.
- Source email.
- Due date (jika tersedia).
- Status.
- Priority.
- Created timestamp.

Status awal:

- Pending.
- In Progress.
- Completed.
- Cancelled.

AI tidak boleh menganggap tanggal yang tidak disebutkan sebagai deadline yang pasti.

## 5.7 Daily Digest

**FR-022 — Daily Email Digest**

Sistem menghasilkan ringkasan aktivitas email harian.

Informasi yang ditampilkan:

- Jumlah email masuk.
- Email penting.
- Email yang membutuhkan balasan.
- Action items.
- Deadline mendatang.
- Ringkasan komunikasi.

**FR-023 — Digest Scheduling**

Sistem mendukung pengaturan jadwal pembuatan digest berdasarkan zona waktu pengguna.

## 5.8 Intelligent Search

**FR-024 — Keyword Search**

Pengguna dapat mencari email berdasarkan kata kunci.

**FR-025 — Semantic Search**

Pengguna dapat mencari email berdasarkan kesamaan makna, bukan hanya kecocokan kata.

**FR-026 — Natural Language Search**

Pengguna dapat melakukan pencarian menggunakan pertanyaan alami.

Contoh:

- "Cari email dari dosen mengenai tugas akhir."
- "Tampilkan email yang meminta saya mengirim dokumen."
- "Cari percakapan mengenai jadwal meeting bulan lalu."
- "Email mana yang memiliki deadline minggu ini?"

**FR-027 — Search Source Reference**

Hasil pencarian harus menyediakan referensi ke email sumber.

## 5.9 AI Conversational Assistant

**FR-028 — Conversational Search**

Pengguna dapat bertanya kepada AI mengenai informasi yang terdapat dalam email.

**FR-029 — Contextual Answer**

AI memberikan jawaban berdasarkan email yang relevan.

**FR-030 — Source Citation**

Jawaban AI menampilkan referensi email yang digunakan sebagai sumber informasi.

**FR-031 — Conversation History**

Sistem dapat menyimpan riwayat percakapan AI milik pengguna.

**FR-032 — Context Isolation**

AI hanya boleh mengakses data email milik pengguna yang sedang terautentikasi.

## 5.10 AI Reply Suggestion

**FR-033 — Reply Draft Generation**

AI dapat membuat draft balasan berdasarkan konteks email.

**FR-034 — Reply Tone Selection**

Pengguna dapat memilih gaya komunikasi:

- Professional.
- Formal.
- Friendly.
- Concise.

**FR-035 — Manual Editing**

Pengguna dapat mengedit hasil draft sebelum digunakan.

**FR-036 — User Confirmation**

Pengiriman email harus membutuhkan tindakan dan konfirmasi eksplisit dari pengguna.

Tidak boleh ada pengiriman otomatis hanya berdasarkan keputusan AI.

---

# 6. Non-Functional Requirements

## 6.1 Performance

- Halaman utama harus memuat data secara bertahap.
- API harus mendukung pagination.
- Proses AI berjalan secara asynchronous apabila membutuhkan waktu lama.
- Sistem menggunakan caching untuk data yang sesuai.
- Embedding dan pencarian semantik menggunakan PostgreSQL + pgvector.

Target awal untuk pengujian:

| Metric | Initial Target |
|---|---|
| API response | p95 < 500 ms untuk endpoint non-AI yang sederhana |
| Dashboard loading | Target < 3 detik pada lingkungan pengujian yang memadai |
| Background jobs | Tidak memblokir request utama |
| Search | Target < 2 detik pada dataset pengujian awal |

Target tersebut merupakan sasaran engineering, bukan jaminan pada semua perangkat dan jaringan.

## 6.2 Scalability

- Mendukung banyak pengguna.
- Menggunakan database indexing.
- Mendukung background task processing.
- Memisahkan proses sinkronisasi dan AI dari request utama.
- Menggunakan provider abstraction untuk mempermudah ekspansi.

## 6.3 Reliability

- Memiliki mekanisme retry untuk pekerjaan asynchronous.
- Menghindari pemrosesan email duplikat.
- Menyimpan status sinkronisasi.
- Menangani kegagalan API eksternal.
- Menyediakan logging dan monitoring.

## 6.4 Maintainability

- Modular monolith pada tahap awal.
- Pemisahan business logic dan integration layer.
- Type-safe frontend.
- Validasi backend menggunakan Pydantic.
- Database migration menggunakan Alembic.
- Automated testing melalui CI.

## 6.5 Accessibility

- Mendukung navigasi keyboard.
- Kontras warna yang memadai.
- Struktur heading yang konsisten.
- Label yang jelas pada input.
- Antarmuka responsif.

---

# 7. Technical Architecture

## 7.1 Architecture Overview

MailMind AI menggunakan arsitektur modular monolith dengan pemisahan frontend, backend, database, worker, dan integrasi eksternal.

```text
                  USER
                   |
          +--------+--------+
          |                 |
       WEB APP         DESKTOP APP
       Next.js           Tauri 2
          |                 |
          +--------+--------+
                   |
                API
                   |
              FastAPI
                   |
        +----------+-----------+
        |          |           |
     Services   Workers    Integrations
        |          |           |
        |        Celery    Gmail API
        |          |        LLM APIs
        |        Redis     OAuth
        |          |
        +----------+-----------+
                   |
              PostgreSQL
                pgvector
```

## 7.2 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js | Web application |
| Language | TypeScript | Type safety |
| Styling | Tailwind CSS | Styling |
| UI Components | shadcn/ui | Interface components |
| Desktop | Tauri 2 | Desktop runtime |
| Backend | FastAPI | REST API |
| Backend Language | Python | Business logic and AI |
| ORM | SQLAlchemy 2 | Database interaction |
| Migration | Alembic | Schema migration |
| Validation | Pydantic | Data validation |
| Database | PostgreSQL | Persistent storage |
| Vector Search | pgvector | Embedding storage and search |
| Cache | Redis | Cache and broker |
| Background Jobs | Celery | Asynchronous processing |
| Containerization | Docker | Development and deployment |
| Version Control | Git + GitHub | Source management |

## 7.3 Architectural Decision

**Modular Monolith**

Pada tahap awal, sistem tidak menggunakan microservices.

Alasan:

1. Mempermudah pengembangan.
2. Mengurangi kompleksitas deployment.
3. Memudahkan debugging.
4. Menghindari overhead komunikasi antarlayanan.
5. Memungkinkan pemisahan layanan ketika kebutuhan sistem berkembang.

---

# 8. AI Architecture

## 8.1 AI Provider Abstraction

MailMind AI tidak boleh bergantung pada satu penyedia model.

Arsitektur AI harus memiliki abstraction layer.

Contoh:

```text
AI Service
    |
LLM Provider Interface
    |
    +-- Gemini Provider
    +-- OpenRouter Provider
    +-- Groq Provider
    +-- Future Providers
```

Provider dapat dipilih berdasarkan konfigurasi dan ketersediaan model.

Gemini menjadi provider utama pada tahap pengembangan awal.

OpenRouter dan Groq menjadi opsi tambahan.

Ketersediaan model, harga, rate limits, dan free tier harus diperiksa berdasarkan ketentuan provider terbaru. Tidak boleh mengasumsikan layanan gratis tersedia tanpa batas.

## 8.2 AI Processing Pipeline

```text
Email Synchronization
        |
Email Normalization
        |
Content Extraction
        |
Preprocessing
        |
AI Analysis
        |
Structured Output Validation
        |
Database Storage
        |
Frontend Display
```

## 8.3 AI Features

Setiap fitur AI harus memiliki service tersendiri:

- Summarization Service.
- Classification Service.
- Priority Detection Service.
- Action Extraction Service.
- Embedding Service.
- Semantic Search Service.
- Conversational Assistant.
- Reply Generation Service.

## 8.4 Retrieval-Augmented Generation

Alur RAG:

1. Email diambil dari provider.
2. Konten dinormalisasi.
3. Email diproses menjadi chunk apabila diperlukan.
4. Embedding dibuat menggunakan embedding model.
5. Embedding disimpan dalam pgvector.
6. Pertanyaan pengguna dikonversi menjadi embedding.
7. Sistem mengambil dokumen relevan dengan filter kepemilikan pengguna.
8. LLM menghasilkan jawaban berdasarkan konteks yang ditemukan.
9. Sistem menampilkan jawaban dan referensi sumber.

Semua retrieval wajib menerapkan filter tenant/user sebelum konteks diberikan ke model.

Dimensi embedding tidak boleh ditentukan secara sembarangan. Dimensi harus mengikuti model embedding yang dipilih dan dikonfigurasi melalui migration atau desain penyimpanan yang sesuai.

## 8.5 Structured AI Output

Hasil AI harus menggunakan struktur data yang tervalidasi.

Contoh:

```json
{
  "summary": "Ringkasan isi email",
  "category": "academic",
  "priority": "high",
  "action_items": [
    {
      "description": "Mengirim dokumen",
      "due_date": null,
      "status": "pending"
    }
  ]
}
```

Backend wajib memvalidasi hasil AI sebelum menyimpan atau menggunakannya.

---

# 9. Database Design

## 9.1 Initial Database Entities

| Table | Description |
|---|---|
| users | Informasi akun pengguna |
| user_settings | Preferensi pengguna |
| email_accounts | Akun email yang terhubung |
| email_threads | Percakapan email |
| email_messages | Pesan email |
| email_labels | Label email |
| ai_analyses | Hasil analisis AI |
| action_items | Tugas hasil ekstraksi |
| email_embeddings | Embedding untuk semantic search |
| sync_states | Status sinkronisasi |
| ai_usage_logs | Catatan penggunaan AI |

## 9.2 Future Entities

| Table | Description |
|---|---|
| digests | Ringkasan harian |
| notifications | Notifikasi pengguna |
| audit_logs | Catatan aktivitas keamanan |
| sync_jobs | Riwayat pekerjaan sinkronisasi |
| ai_conversations | Percakapan AI |
| ai_messages | Pesan dalam percakapan AI |

## 9.3 Data Relationship

Relasi utama:

- One user can have multiple email accounts.
- One email account can have multiple email threads.
- One email thread can have multiple email messages.
- One email message can have multiple AI analyses over time.
- One user can have multiple action items.
- One email message can have multiple embeddings or chunks.
- One user can have multiple AI conversations.

## 9.4 Database Rules

- Gunakan UUID sebagai primary key.
- Gunakan foreign key untuk menjaga integritas relasi.
- Terapkan index pada kolom yang sering digunakan.
- Terapkan user ownership pada setiap data privat.
- Gunakan timestamp dengan timezone yang konsisten.
- Hindari menyimpan OAuth token dalam bentuk plaintext.
- Tentukan kebijakan retensi dan penghapusan data.

Row-Level Security (RLS) dapat digunakan sebagai lapisan pertahanan tambahan. Jika menggunakan connection pooling, desain konteks user dan transaksi harus memastikan identitas tenant tidak bocor antarsesi.

---

# 10. API Design

API menggunakan REST dengan versioning.

Base URL:

```text
/api/v1
```

## 10.1 Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Registrasi |
| POST | /auth/login | Login |
| POST | /auth/logout | Logout |
| GET | /auth/me | Informasi pengguna |

## 10.2 Email Accounts

| Method | Endpoint | Description |
|---|---|---|
| GET | /accounts | Daftar akun email |
| POST | /accounts/gmail/connect | Memulai koneksi Gmail |
| GET | /accounts/gmail/callback | OAuth callback |
| DELETE | /accounts/{id} | Memutus koneksi akun |

## 10.3 Emails

| Method | Endpoint | Description |
|---|---|---|
| GET | /emails | Daftar email |
| GET | /emails/{id} | Detail email |
| GET | /emails/{id}/thread | Detail percakapan |
| POST | /emails/sync | Memulai sinkronisasi |
| GET | /emails/search | Pencarian email |

## 10.4 AI

| Method | Endpoint | Description |
|---|---|---|
| POST | /ai/summarize | Ringkasan email |
| POST | /ai/classify | Klasifikasi email |
| POST | /ai/prioritize | Deteksi prioritas |
| POST | /ai/extract-actions | Ekstraksi tugas |
| POST | /ai/chat | Percakapan AI |
| POST | /ai/reply-draft | Membuat draft balasan |
| GET | /ai/usage | Penggunaan AI |

## 10.5 Action Items

| Method | Endpoint | Description |
|---|---|---|
| GET | /actions | Daftar tindakan |
| POST | /actions | Membuat tindakan |
| PATCH | /actions/{id} | Memperbarui tindakan |
| DELETE | /actions/{id} | Menghapus tindakan |

API harus menerapkan autentikasi, otorisasi, validasi input, pagination, dan pembatasan penggunaan sesuai kebutuhan.

---

# 11. Security and Privacy Requirements

Keamanan merupakan persyaratan utama karena aplikasi memproses komunikasi pribadi pengguna.

## 11.1 Authentication Security

- Gunakan mekanisme autentikasi yang aman.
- Terapkan session expiration.
- Lindungi endpoint menggunakan authentication middleware.
- Terapkan rate limiting pada endpoint sensitif.
- Jangan menyimpan password dalam plaintext.

## 11.2 OAuth Security

- Gunakan OAuth 2.0 Authorization Code Flow.
- Terapkan state validation.
- Gunakan PKCE apabila sesuai dengan jenis client.
- Simpan token secara terenkripsi.
- Jangan menampilkan access token atau refresh token pada frontend.
- Sediakan mekanisme revocation dan disconnect.
- Hindari meminta permission yang tidak diperlukan.

Untuk Gmail, gunakan scope dengan hak akses minimum.

Scope Gmail `gmail.readonly` merupakan restricted scope. Distribusi publik aplikasi yang menggunakan restricted scopes dapat memerlukan proses verifikasi Google dan security assessment sesuai ketentuan Google yang berlaku.

Kebutuhan persetujuan dan verifikasi harus diperiksa sebelum aplikasi dirilis untuk pengguna publik.

## 11.3 Data Isolation

Setiap pengguna hanya dapat mengakses data miliknya.

Persyaratan:

- Semua query harus memperhatikan user ownership.
- Validasi kepemilikan resource pada backend.
- Terapkan isolasi tenant.
- Jangan mengandalkan filter frontend.
- Uji akses lintas akun secara otomatis.

## 11.4 AI Security

Isi email merupakan input tidak tepercaya.

Sistem harus melindungi aplikasi dari prompt injection yang berasal dari konten email.

Persyaratan:

1. Isi email tidak boleh dianggap sebagai system instruction.
2. Model tidak boleh diberikan akses langsung terhadap secret atau credential.
3. Output AI harus divalidasi.
4. Tool execution harus dibatasi.
5. AI tidak boleh mengirim email atau menghapus data tanpa persetujuan pengguna.
6. Referensi sumber harus dapat ditelusuri.
7. Konten email yang tidak tepercaya harus dipisahkan dari instruksi sistem.

## 11.5 Cloud AI Privacy

Sebelum menggunakan cloud AI provider, sistem harus:

- Memberikan informasi kepada pengguna bahwa konten email dapat dikirim ke provider AI.
- Menyediakan pengaturan persetujuan penggunaan cloud AI.
- Menjelaskan data apa yang diproses.
- Menjelaskan provider yang digunakan.
- Menghindari pengiriman data yang tidak diperlukan.
- Menyediakan pilihan menonaktifkan fitur AI berbasis cloud.

Jangan mengklaim bahwa provider tidak menyimpan atau menggunakan data untuk pelatihan tanpa memverifikasi kebijakan provider dan konfigurasi layanan yang digunakan.

## 11.6 Logging

- Jangan mencatat password.
- Jangan mencatat OAuth token.
- Hindari menyimpan isi email secara penuh dalam application logs.
- Catat error dengan informasi yang cukup untuk debugging.
- Lindungi audit log dari akses yang tidak sah.

## 11.7 User Control

Pengguna harus dapat:

- Memutus koneksi akun email.
- Menghapus data yang tersimpan.
- Mengatur penggunaan AI.
- Melihat penggunaan AI.
- Mengelola preferensi.
- Mengelola riwayat percakapan AI.

---

# 12. UI/UX Requirements

## 12.1 Main Dashboard

Komponen utama:

- Sidebar navigation.
- Top navigation.
- Email overview.
- Important emails.
- Pending actions.
- AI daily digest.
- Search bar.
- AI assistant entry point.

## 12.2 Navigation

Menu utama:

1. Dashboard.
2. Inbox.
3. Important.
4. Action Items.
5. AI Assistant.
6. Search.
7. Settings.

## 12.3 Design Principles

- Minimalist.
- Professional.
- Responsive.
- Readable.
- Consistent.
- Accessible.
- Information hierarchy yang jelas.

## 12.4 UI Components

Gunakan shadcn/ui untuk:

- Buttons.
- Dialogs.
- Dropdowns.
- Cards.
- Tables.
- Forms.
- Tabs.
- Tooltips.
- Toast notifications.
- Command menu.

---

# 13. Background Processing

Celery dan Redis digunakan untuk pekerjaan yang tidak perlu diproses langsung dalam HTTP request.

Jenis pekerjaan:

| Job | Description |
|---|---|
| Email Sync | Sinkronisasi email |
| Email Processing | Normalisasi email |
| AI Summarization | Ringkasan email |
| Classification | Klasifikasi email |
| Embedding Generation | Pembuatan embedding |
| Daily Digest | Pembuatan digest |
| Retry Failed Jobs | Pemrosesan ulang pekerjaan gagal |

Persyaratan:

- Task harus memiliki status.
- Task harus mendukung retry dengan batas percobaan.
- Task harus idempotent apabila memungkinkan.
- Hindari pemrosesan ganda.
- Simpan error metadata yang aman.
- Gunakan scheduling untuk pekerjaan berkala.

---

# 14. Testing Requirements

## 14.1 Backend Testing

- Unit testing.
- Integration testing.
- API testing.
- Authentication testing.
- Authorization testing.
- Database testing.

## 14.2 Frontend Testing

- Component testing.
- Form validation testing.
- Navigation testing.
- Error state testing.
- Responsive testing.

## 14.3 AI Testing

- Summarization quality.
- Classification accuracy.
- Priority detection quality.
- Action extraction accuracy.
- Retrieval relevance.
- Grounded answer evaluation.
- Prompt injection resistance.
- Hallucination evaluation.

AI tidak cukup dievaluasi hanya menggunakan HTTP status 200 atau keberhasilan pemanggilan model.

## 14.4 Security Testing

- Cross-user access testing.
- OAuth callback validation.
- Token exposure testing.
- SQL injection testing.
- XSS testing.
- CSRF testing sesuai mekanisme autentikasi.
- Rate limit testing.
- Prompt injection testing.

---

# 15. Deployment and Infrastructure

## 15.1 Development Environment

Gunakan Docker Compose untuk menjalankan layanan utama.

Komponen:

- Web frontend.
- FastAPI backend.
- PostgreSQL + pgvector.
- Redis.
- Celery worker.

## 15.2 Environment Variables

Contoh `.env.example`:

```env
APP_ENV=development
APP_NAME=MailMind AI

WEB_PORT=3000
API_PORT=8000

DATABASE_URL=postgresql+psycopg://user:password@db:5432/mailmind
REDIS_URL=redis://redis:6379/0

SECRET_KEY=replace_me

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

GEMINI_API_KEY=
OPENROUTER_API_KEY=
GROQ_API_KEY=
```

Nilai tersebut merupakan contoh konfigurasi. File `.env` aktual tidak boleh dimasukkan ke Git.

## 15.3 Deployment Strategy

Tahapan deployment:

1. Local development.
2. Development testing.
3. Staging deployment.
4. Production deployment.

Produksi harus menggunakan HTTPS, secret management yang layak, database backup, monitoring, dan konfigurasi akses yang aman.

---

# 16. Project Roadmap

Estimasi awal pengembangan: 8–10 minggu.

Estimasi ini merupakan rencana awal dan dapat berubah sesuai kompleksitas integrasi, ketersediaan API, dan hasil pengujian.

## Phase 1 — Foundation

**Target: Minggu 1–2**

Fokus: menyiapkan fondasi aplikasi.

Tasks:

- [ ] Repository structure.
- [ ] Monorepo setup.
- [ ] Next.js initialization.
- [ ] FastAPI initialization.
- [ ] PostgreSQL + pgvector.
- [ ] Redis setup.
- [ ] Celery setup.
- [ ] Docker Compose.
- [ ] Initial database migration.
- [ ] Health check endpoint.
- [ ] `.env.example`.
- [ ] `.gitignore`.
- [ ] Initial README.
- [ ] Development documentation.

**Deliverable:** Aplikasi dapat dijalankan secara lokal melalui Docker Compose dengan frontend, backend, database, dan worker yang berfungsi.

Catatan: Sprint ini belum mencakup Gmail OAuth maupun implementasi fitur AI.

## Phase 2 — Authentication and Email Integration

**Target: Minggu 3**

Tasks:

- [ ] User registration.
- [ ] User login.
- [ ] Session management.
- [ ] Google OAuth.
- [ ] Gmail API integration.
- [ ] Account connection.
- [ ] Email synchronization.
- [ ] Email storage.
- [ ] Basic inbox.

**Deliverable:** Pengguna dapat menghubungkan Gmail dan melihat email pada MailMind AI.

## Phase 3 — Email Management

**Target: Minggu 4**

Tasks:

