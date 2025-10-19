-- Supabase 데이터베이스 스키마
-- 이 파일을 Supabase SQL Editor에서 실행하세요

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    school TEXT,
    role TEXT DEFAULT 'teacher' CHECK (role IN ('teacher', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- 생성된 자료를 저장하는 테이블
CREATE TABLE IF NOT EXISTS generated_materials (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    unit_data JSONB NOT NULL,
    generated_content JSONB NOT NULL,
    quality_check JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 사용자 평가 결과를 저장하는 테이블
CREATE TABLE IF NOT EXISTS evaluation_results (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID REFERENCES generated_materials(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    section TEXT,
    score INTEGER,
    accuracy TEXT,
    fluency TEXT,
    grammar TEXT,
    feedback TEXT,
    individual_scores JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Rewrite 활동 결과를 저장하는 테이블
CREATE TABLE IF NOT EXISTS rewrite_activities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID REFERENCES generated_materials(id) ON DELETE CASCADE,
    activity_type TEXT NOT NULL, -- 'vocabulary_fill' or 'full_rewrite'
    original_story TEXT NOT NULL,
    modified_story TEXT,
    blanks JSONB,
    student_answer TEXT,
    score JSONB,
    total_score FLOAT,
    feedback JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 음성 전사 결과를 저장하는 테이블
CREATE TABLE IF NOT EXISTS transcriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID REFERENCES generated_materials(id) ON DELETE CASCADE,
    audio_filename TEXT,
    transcription TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_generated_materials_created_at ON generated_materials(created_at);
CREATE INDEX IF NOT EXISTS idx_evaluation_results_material_id ON evaluation_results(material_id);
CREATE INDEX IF NOT EXISTS idx_rewrite_activities_material_id ON rewrite_activities(material_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_material_id ON transcriptions(material_id);

-- RLS (Row Level Security) 정책 설정
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE evaluation_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE rewrite_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE transcriptions ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기/쓰기 가능하도록 설정 (실제 운영에서는 인증 기반으로 변경)
CREATE POLICY "Allow all operations on users" ON users
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on generated_materials" ON generated_materials
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on evaluation_results" ON evaluation_results
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on rewrite_activities" ON rewrite_activities
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on transcriptions" ON transcriptions
    FOR ALL USING (true);
