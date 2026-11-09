const SUPABASE_URL = "https://efoihtyqwiozogxaidbg.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_hRgSkA4z4_msy0PBeUZ0gQ_LKb_yY8H";

window.supabaseClient = window.supabase.createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);
