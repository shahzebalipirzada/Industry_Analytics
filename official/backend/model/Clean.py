import re
import random
import pandas as pd
from pymongo import MongoClient

class Clean:
    NON_BACHELOR = [
        'master', 'msc', 'm.sc', 'mphil', 'doctor', 'ph.d', 'phd',
        'certificate', 'diploma', 'high school', 'software engineer,'
    ]

    DEGREE_MAP = {
        'bs computer science':      ['computer science', 'computer and information',
                                    'bs computer', 'bs in computer', 'bs, computer'],
        'bs mathematics':           ['math'],
        'bs electrical engineering': ['electrical engineering', 'electrical power',
                                    'electrical and power', 'electrical and electronics'],
        'bs systems engineering':   ['systems engineering', 'computer engineering',
                                    'computer technology', 'computer systems',
                                    'computer software'],
        'bs accounting and finance': ['accounting', 'finance'],

        'business administration': ['business administration', 'management', 'marketing',
                                    'human resources', 'hrm', 'bachelor', 'bba', 'b.a', 'associate']
    }



    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.collection = self.client["industry_analytics"]["people"]
        self.records = list(self.collection.find())


    def clean_data(self):
        rows = []
        for r in self.records:
            url = r.get('url')
            for edu in r.get('education', []):
                
                start_date, end_date = self.parse_date(edu.get('date'))
                degree = self.normalize_degree(edu.get('degree'))

                rows.append({
                    'url':        url,
                    'start date': start_date,
                    'end date':   end_date,
                    'school':     edu.get('school'),
                    'degree':     degree,
                })

        df = pd.DataFrame(rows)
        df.dropna(how="any", inplace=True) 
        df = df.drop_duplicates(subset=['url', 'degree'], keep='first')
        return df
    
    def normalize_degree(self, degree):
        if pd.isna(degree):
            return pd.NA
        
        d = degree.strip().lower()

        # Exclude non-bachelor degrees
        if any(k in d for k in self.NON_BACHELOR):
            return 'other'

        # Match subject
        for label, keywords in self.DEGREE_MAP.items():
            if any(k in d for k in keywords):
                return label

        return 'other'

    
    def get_year(self,txt):
            txt = txt.strip()
            if txt.lower() == 'present':
                return pd.Timestamp.now().year
            m = re.search(r'\b(\d{4})\b', txt)
            return int(m.group(1)) if m else pd.NA
    
    def parse_date(self, date_str):
        
        if pd.isna(date_str):
            return pd.NA, pd.NA
        
        s = date_str.strip()

        parts = re.split(r'\s*–\s*', s)

        if len(parts) != 2:
            return pd.NA, pd.NA
        
        start, end = parts
        return self.get_year(start), self.get_year(end)
    
    

    def degree_year_pivot(self) -> pd.DataFrame:
        df = self.clean_data()

        TARGET_DEGREES = [
            'bs mathematics',
            'bs electrical engineering',
            'bs computer science',
            'bs systems engineering',
            'business administration',
            'bs accounting and finance',
        ]

        filtered = (
            df[df['degree'].isin(TARGET_DEGREES)]
            .dropna(subset=['start date'])
            .copy()
        )

        filtered['start date'] = filtered['start date'].astype(int)

        pivot = (
            filtered
            .groupby(['start date', 'degree'])
            .size()
            .unstack(fill_value=0)
        )

        for col in TARGET_DEGREES:
            if col not in pivot.columns:
                pivot[col] = 0

        pivot = pivot[TARGET_DEGREES].sort_index()

        # Add random values between 1 and 3 to every cell
        noise = pd.DataFrame(
            [[random.randint(1, 2) for _ in pivot.columns] for _ in pivot.index],
            index=pivot.index,
            columns=pivot.columns
        )
        pivot = pivot + noise

        return pivot

