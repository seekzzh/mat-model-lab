"""
Material Database Utility

Provides functions to load, query, and save material data from JSON database.
"""

import json
import os
import sys

def get_database_path():
    """Get the path to the materials database file."""
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, 'assets', 'database', 'materials.json')


class MaterialDatabase:
    """Class to manage material database operations."""
    
    def __init__(self):
        self.db_path = get_database_path()
        self.data = {
            "elastic": [],
            "plastic": [],
            "hyperelastic": []
        }
        self.load()
    
    def load(self):
        """Load materials from JSON file."""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"MaterialDatabase: Loaded {self.count_all()} materials from {self.db_path}")
            else:
                print(f"MaterialDatabase: Database file not found at {self.db_path}, using empty database.")
        except Exception as e:
            print(f"MaterialDatabase: Error loading database: {e}")
    
    def save(self):
        """Save materials to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"MaterialDatabase: Saved to {self.db_path}")
            return True
        except Exception as e:
            print(f"MaterialDatabase: Error saving database: {e}")
            return False
    
    def get_all(self):
        """Get all materials as a flat list."""
        result = []
        for category, materials in self.data.items():
            for mat in materials:
                mat_copy = mat.copy()
                mat_copy['category'] = category
                result.append(mat_copy)
        return result
    
    def get_by_category(self, category):
        """Get materials by category (elastic, plastic, hyperelastic).
        
        Parameters
        ----------
        category : str
            Category name ('elastic', 'plastic', 'hyperelastic')
            
        Returns
        -------
        list
            List of material dictionaries
        """
        return self.data.get(category, [])
    
    def search(self, query, category=None):
        """Search materials by name (case-insensitive).
        
        Parameters
        ----------
        query : str
            Search query string
        category : str, optional
            Limit search to specific category
            
        Returns
        -------
        list
            List of matching material dictionaries
        """
        query_lower = query.lower()
        if category:
            materials = self.get_by_category(category)
            return [m for m in materials if query_lower in m.get('name', '').lower()]
        else:
            all_materials = self.get_all()
            return [m for m in all_materials if query_lower in m.get('name', '').lower()]
    
    def add_material(self, category, material):
        """Add a new material to the database.
        
        Parameters
        ----------
        category : str
            Category to add to ('elastic', 'plastic', 'hyperelastic')
        material : dict
            Material data dictionary with keys: name, crystal_type, cij, source, description
            
        Returns
        -------
        bool
            True if successful
        """
        if category not in self.data:
            self.data[category] = []
        self.data[category].append(material)
        return self.save()
    
    def delete_material(self, category, name):
        """Delete a material by name.
        
        Parameters
        ----------
        category : str
            Category to delete from
        name : str
            Material name to delete
            
        Returns
        -------
        bool
            True if found and deleted
        """
        if category in self.data:
            original_len = len(self.data[category])
            self.data[category] = [m for m in self.data[category] if m.get('name') != name]
            if len(self.data[category]) < original_len:
                self.save()
                return True
        return False
    
    def count_all(self):
        """Count total number of materials."""
        return sum(len(materials) for materials in self.data.values())


# Singleton instance for easy access
_db_instance = None

def get_database():
    """Get the singleton MaterialDatabase instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = MaterialDatabase()
    return _db_instance
