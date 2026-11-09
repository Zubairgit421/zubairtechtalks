const SUPABASE_URL = "https://efoihtyqwiozogxaidbg.supabase.co";
const SUPABASE_ANON_KEY = "YOUR_ACTUAL_PUBLISHABLE_KEY";

window.supabaseClient = window.supabase.createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);
