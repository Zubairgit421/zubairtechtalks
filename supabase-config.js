
const SUPABASE_URL = "https://cgnqgmukuewplezhtljh.supabase.co";

const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_w2OtgrzEYA_YOxwW8fgBog_CAplG7da";

window.supabaseClient = window.supabase.createClient(
  SUPABASE_URL,
  SUPABASE_PUBLISHABLE_KEY
);
