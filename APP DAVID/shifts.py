from supabase import create_client, Client
import json
from datetime import datetime
from typing import Dict, List, Optional

class ShiftManager:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    def create_table(self):
        """Create shifts table if not exists"""
        response = self.supabase.table('shifts').select('*').limit(1).execute()
        if response.data:  
            print("Table shifts sudah ada")
            return
        
        # Create table via RPC or SQL editor, but for now assume manual
        print("Buat table 'shifts' manual di Supabase SQL Editor:")
        print("""
CREATE TABLE shifts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  shift1 JSONB,
  shift2 JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
""")
    
    def save_shift(self, shift1: List[str], shift2: List[str]) -> Optional[str]:
        """Save shift data, return id"""
        data = {
            "shift1": json.dumps(shift1),
            "shift2": json.dumps(shift2)
        }
        response = self.supabase.table('shifts').insert(data).execute()
        if response.data:
            return response.data[0]['id']
        return None
    
    def get_shifts(self) -> List[Dict]:
        """Get all shifts"""
        response = self.supabase.table('shifts').select('*').order('created_at', desc=True).execute()
        return response.data or []
    
    def delete_shift(self, shift_id: str) -> bool:
        """Delete shift by id"""
        response = self.supabase.table('shifts').delete().eq('id', shift_id).execute()
        return len(response.data) > 0
