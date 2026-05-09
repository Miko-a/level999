# HSR RAG Chatbot

HSR RAG Chatbot adalah aplikasi website chatbot berbasis **Retrieval-Augmented Generation (RAG)** untuk membantu pemain **Honkai: Star Rail** memahami konsep dasar game seperti team building, relic, Light Cone, Trace priority, Path, Element, farming priority, dan survival guide.

Project ini dipisahkan menjadi dua bagian utama:

```text
hsr-rag-chatbot/
  frontend/   # Next.js application
  backend/    # FastAPI application
```

Backend menggunakan **FastAPI** untuk menyediakan API chat, knowledge management, dan semantic retrieval. Frontend menggunakan **Next.js** untuk menampilkan chat UI dan halaman admin. Sistem RAG menggunakan local Markdown knowledge base, local embedding model, dan ChromaDB sebagai vector database.

---

## 1. Fitur Utama

### Chatbot HSR

User dapat bertanya tentang konsep dasar Honkai: Star Rail, misalnya:

```text
Apa itu relic di HSR?
Bagaimana cara membuat tim untuk pemula?
Aku sering mati di battle, harus upgrade apa dulu?
Light Cone lebih penting atau relic dulu?
Apa bedanya Path dan Element?
```

Chatbot akan mencari konteks dari knowledge base lokal, lalu menghasilkan jawaban berdasarkan konteks tersebut.

### Semantic RAG

Sistem tidak hanya mencari keyword yang sama, tetapi menggunakan embedding untuk menemukan dokumen yang maknanya relevan.

Alur RAG:

```text
User question
   |
   v
Embedding query
   |
   v
Search similar chunks in ChromaDB
   |
   v
Build RAG context
   |
   v
Generate answer with LLM / mock LLM
   |
   v
Return answer + sources
```

### Source Display

Setiap jawaban menampilkan source yang digunakan, termasuk:

```text
Title
File name
Chunk ID
Category
Topic
Version
Similarity score
Preview
```

### Admin Knowledge Manager

Aplikasi memiliki halaman admin untuk mengelola knowledge base lokal.

Admin dapat:

```text
Melihat daftar file knowledge base
Membuat file Markdown knowledge baru
Menghapus file knowledge
Melakukan re-ingestion ke vector database
Melihat jumlah chunk di ChromaDB
```

Halaman admin diproteksi dengan login sederhana.

Credential demo:

```text
Username: admin
Password: admin123
```

<img width="1039" height="914" alt="image" src="https://github.com/user-attachments/assets/07fab472-127f-4e47-a11f-c52bc735de1a" />


---

## 2. Tech Stack

### Frontend

```text
Next.js
React
TypeScript
Tailwind CSS
```

### Backend

```text
FastAPI
Python
Pydantic
Uvicorn
python-dotenv
```

### RAG / Vector Search

```text
ChromaDB
SentenceTransformers
all-MiniLM-L6-v2 embedding model
Markdown knowledge base
```

### LLM

```text
Google Gemini API via Google AI Studio
```

---

## 3. Project Structure

```text
hsr-rag-chatbot/
  frontend/
    src/
      app/
        page.tsx
        admin/
          page.tsx
          AdminClient.tsx
          login/
            page.tsx
        api/
          admin/
            login/
              route.ts
            logout/
              route.ts
    proxy.ts
    .env.local
    package.json

  backend/
    app/
      main.py
      routes/
        chat.py
        knowledge.py
      schemas/
        chat_schema.py
        knowledge_schema.py
      services/
        gemini_service.py
        prompt_service.py
        vector_store_service.py
        knowledge_service.py
      scripts/
        ingest_knowledge.py
      knowledge/
        beginner-guide.md
        relic-basics.md
        team-building-basics.md
        path-and-element.md
        farming-priority.md
        light-cone-basics.md
        trace-priority.md
        survival-guide.md
        damage-dealer-basics.md
        support-basics.md
        team-archetypes.md
      vector_db/
    .env
    .env.example
    requirements.txt
```

---

## 4. Backend Setup

Masuk ke folder backend:

```bash
cd backend
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Jika `requirements.txt` belum ada atau belum lengkap, install manual:

```bash
pip install fastapi uvicorn python-dotenv google-genai chromadb sentence-transformers
```

Lalu simpan dependencies:

```bash
pip freeze > requirements.txt
```

---

## 5. Backend Environment Variables

Buat file:

```text
backend/.env
```

Isi:

```env
GEMINI_API_KEY=your_gemini_api_key_here
USE_MOCK_LLM=true
```

Keterangan:

```text
GEMINI_API_KEY   API key dari Google AI Studio.
USE_MOCK_LLM     Jika true, backend tidak memanggil Gemini API.
```

Untuk development tanpa menggunakan Gemini API, gunakan:

```env
USE_MOCK_LLM=true
```

Untuk menggunakan Gemini API:

```env
USE_MOCK_LLM=false
```

---

## 6. Menjalankan Backend

Dari folder `backend/`:

```bash
uvicorn app.main:app --reload
```

Backend berjalan di:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 7. Frontend Setup

Masuk ke folder frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Buat file:

```text
frontend/.env.local
```

Isi:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_SESSION_VALUE=hsr-admin-session
```

---

## 8. Menjalankan Frontend

Dari folder `frontend/`:

```bash
npm run dev
```

Frontend berjalan di:

```text
http://localhost:3000
```

Halaman chatbot:

```text
http://localhost:3000
```

Halaman admin:

```text
http://localhost:3000/admin
```

Halaman login admin:

```text
http://localhost:3000/admin/login
```

---

## 9. Knowledge Base

Knowledge base disimpan sebagai file Markdown di:

```text
backend/app/knowledge/
```

Contoh format dokumen:

```markdown
# Break Effect Basics

Source ID: break-effect-basics
Category: combat
Topic: break effect basics
Game: Honkai: Star Rail
Version: internal-demo
Tags: break, toughness, weakness, beginner

Break Effect is related to weakness breaking. When a character attacks an enemy with a matching Element, the enemy's toughness can be reduced.

For beginners, weakness breaking is useful because it can delay enemies and create safer combat situations.
```

Metadata yang disarankan:

```text
Source ID   ID unik untuk dokumen
Category    Kategori dokumen, misalnya combat, equipment, role, team
Topic       Topik utama dokumen
Game        Nama game
Version     Versi knowledge, misalnya internal-demo atau patch tertentu
Tags        Keyword tambahan untuk membantu retrieval
```

---

## 10. Ingestion Knowledge Base

Setiap kali menambah, mengubah, atau menghapus file di `backend/app/knowledge/`, jalankan ulang ingestion agar ChromaDB diperbarui.

Dari folder `backend/`:

```bash
python -m app.scripts.ingest_knowledge
```

Output yang sehat kira-kira:

```text
Ingested 12 chunks into Chroma collection.
- beginner-guide-0 | general | beginner basics | beginner-guide.md
- relic-basics-0 | general | relics | relic-basics.md
- light-cone-basics-0 | equipment | light cone basics | light-cone-basics.md
```

Vector database lokal disimpan di:

```text
backend/app/vector_db/
```

Folder ini merupakan hasil indexing dan tidak perlu dimasukkan ke Git.

---

## 11. Admin Knowledge Manager

Admin page tersedia di:

```text
http://localhost:3000/admin
```

Jika belum login, user akan diarahkan ke:

```text
http://localhost:3000/admin/login?from=/admin
```

Credential demo:

```text
Username: admin
Password: admin123
```

Fitur admin:

```text
List knowledge files
Create new knowledge file
Delete knowledge file
Re-ingest vector database
View ChromaDB chunk count
```

Setelah membuat atau menghapus knowledge file dari admin page, klik tombol:

```text
Re-ingest
```

Agar dokumen baru masuk ke vector database.

---

## 12. API Endpoints

### Chat

```http
POST /api/chat
```

Request:

```json
{
  "message": "Apa itu relic di HSR?"
}
```

Response:

```json
{
  "answer": "Berdasarkan knowledge base lokal...",
  "sources": [
    {
      "title": "Relic Basics",
      "source_id": "relic-basics",
      "file_name": "relic-basics.md",
      "chunk_id": "relic-basics-0",
      "category": "general",
      "topic": "relics",
      "version": "internal-demo",
      "score": 0.7214,
      "preview": "Relics are equipment pieces..."
    }
  ]
}
```

### Knowledge Files

```http
GET /api/knowledge
```

Mengambil daftar file knowledge base.

```http
POST /api/knowledge
```

Membuat file knowledge baru.

Request:

```json
{
  "file_name": "break-effect-basics.md",
  "title": "Break Effect Basics",
  "source_id": "break-effect-basics",
  "category": "combat",
  "topic": "break effect basics",
  "version": "internal-demo",
  "tags": "break, toughness, weakness, beginner",
  "content": "Break Effect is related to weakness breaking..."
}
```

```http
DELETE /api/knowledge/{file_name}
```

Menghapus file knowledge base.

```http
POST /api/knowledge/reingest
```

Melakukan re-ingestion semua file Markdown ke ChromaDB.

```http
GET /api/knowledge/stats
```

Mengambil statistik vector database.

---

## 13. Authentication

Admin login menggunakan cookie sederhana bernama:

```text
admin_session
```

Login diproses oleh:

```text
frontend/src/app/api/admin/login/route.ts
```

Logout diproses oleh:

```text
frontend/src/app/api/admin/logout/route.ts
```

Halaman `/admin` dilindungi oleh server-side guard di:

```text
frontend/src/app/admin/page.tsx
```

Jika cookie tidak valid, user diarahkan ke:

```text
/admin/login?from=/admin
```

Catatan keamanan:

Sistem login ini hanya cocok untuk local development dan demo. Untuk production, perlu sistem autentikasi yang lebih aman, misalnya JWT, OAuth, database user, password hashing, CSRF protection, dan proteksi API backend.

---

## 14. Development Flow

Workflow umum saat mengembangkan knowledge base:

```text
1. Tambahkan file Markdown ke backend/app/knowledge/
2. Jalankan python -m app.scripts.ingest_knowledge
3. Jalankan backend dengan uvicorn app.main:app --reload
4. Jalankan frontend dengan npm run dev
5. Test pertanyaan dari halaman chatbot
6. Periksa sources yang muncul
7. Perbaiki isi knowledge base jika retrieval belum akurat
```

Jika memakai admin page:

```text
1. Login ke /admin
2. Buat knowledge file baru
3. Klik Re-ingest
4. Kembali ke halaman chatbot
5. Test pertanyaan terkait dokumen baru
```

---

## 15. Contoh Pertanyaan untuk Testing

```text
Apa itu relic di HSR?
Bagaimana cara membuat team untuk pemula?
Aku sering mati di battle, harus upgrade apa dulu?
Light Cone lebih penting atau relic dulu?
Apa bedanya Path dan Element?
Trace apa yang harus dinaikkan dulu?
Kenapa timku tidak boleh semua DPS?
Apa itu Break Effect?
```

Expected behavior:

```text
Pertanyaan umum harus mengambil source relevan dari knowledge base.
Pertanyaan karakter spesifik atau patch-current harus dijawab hati-hati.
Sistem tidak boleh mengarang build terbaru jika data tidak ada di knowledge base.
```

Contoh pertanyaan yang seharusnya ditolak atau diberi batasan:

```text
Build terbaik Castorice patch sekarang apa?
Tier list DPS terbaru siapa?
Relic BiS karakter tertentu apa?
```

Jika data karakter atau patch belum ada di knowledge base, chatbot harus menjelaskan bahwa knowledge base belum cukup.

---

## 16. Current Limitations

Project ini masih MVP dan memiliki beberapa batasan:

```text
Knowledge base masih kecil dan bersifat internal-demo
Belum patch-aware secara real-time
Belum punya data karakter lengkap
Belum mengambil data dari sumber resmi secara otomatis
Admin login belum production-grade
Backend knowledge API belum dilindungi auth
Belum ada database user
Belum ada chat history permanen
Belum ada streaming response
Belum ada upload file knowledge dari UI
```

---

## 17. Status Project

Project saat ini sudah mendukung:

```text
Frontend chat UI
FastAPI backend
Gemini API integration
Mock LLM fallback
Local Markdown knowledge base
Semantic vector retrieval with ChromaDB
Source display
Admin knowledge manager
Admin login page
Server-side admin page guard
```

Dengan fitur tersebut, project sudah cukup untuk disebut sebagai **MVP RAG chatbot untuk Honkai: Star Rail**.

### Screenshot:

<img width="798" height="906" alt="image" src="https://github.com/user-attachments/assets/f914e139-3a00-4982-ae6e-f39a42d6692c" />

<img width="806" height="716" alt="image" src="https://github.com/user-attachments/assets/2c3c1859-9cd5-4438-abfb-06642902cc03" />

<img width="762" height="903" alt="image" src="https://github.com/user-attachments/assets/8c3c2eee-c85a-47ef-842e-9e441847e7f6" />

