#!/usr/bin/env python
"""Initialize PostgreSQL database with tables and seed data"""

from app.db.session import engine
from app.db.base import Base
from app.db.seeder import seed_db
from app.db.session import SessionLocal

def init_db():
    print('🔧 Creating PostgreSQL tables...')
    Base.metadata.create_all(bind=engine)
    print('✅ Tables created successfully')

    print('\n📋 Seeding database with sample data...')
    db = SessionLocal()
    seed_db(db)
    db.close()
    print('✅ Database seeded successfully')
    
    print('\n🎉 PostgreSQL database initialized!')
    print('📝 Test credentials:')
    print('   Email: carlos@cliente.com')
    print('   Password: pas12345')

if __name__ == '__main__':
    init_db()
