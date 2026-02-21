-- Fix Row Level Security (RLS) - Run this in Supabase SQL Editor

-- Option 1: Disable RLS (for development/testing)
ALTER TABLE rumor_sources DISABLE ROW LEVEL SECURITY;
ALTER TABLE risk_analysis DISABLE ROW LEVEL SECURITY;

-- Option 2: OR create permissive policy (if you want RLS enabled)
-- DROP POLICY IF EXISTS "Allow all operations" ON rumor_sources;
-- DROP POLICY IF EXISTS "Allow all operations" ON risk_analysis;

-- CREATE POLICY "Enable all for anon" ON rumor_sources FOR ALL TO anon USING (true) WITH CHECK (true);
-- CREATE POLICY "Enable all for anon" ON risk_analysis FOR ALL TO anon USING (true) WITH CHECK (true);
