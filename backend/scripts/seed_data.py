"""
Örnek veri yükleme scripti
"""
import sys
from pathlib import Path

# Backend dizinini Python path'ine ekle
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import create_db_and_tables, engine
from app.models import User, Project, Experiment, Entry, Template
from sqlmodel import Session


def seed_data():
    """Örnek verileri veritabanına yükle"""
    create_db_and_tables()
    
    with Session(engine) as session:
        # Kullanıcılar
        users = [
            User(name="Dr. Ahmet Yılmaz", email="ahmet@example.com", role="researcher"),
            User(name="Dr. Ayşe Kara", email="ayse@example.com", role="researcher"),
            User(name="Prof. Mehmet Demir", email="mehmet@example.com", role="admin"),
        ]
        for user in users:
            session.add(user)
        session.commit()
        
        print(f"✅ {len(users)} kullanıcı oluşturuldu")
        
        # Projeler
        projects = [
            Project(
                name="YBCO İnce Film Karakterizasyonu",
                description="YBa2Cu3O7-δ ince film örneklerin elektriksel ve manyetik özellikleri",
                tags=["YBCO", "ince film", "süperiletken"],
                created_by=users[0].id,
            ),
            Project(
                name="Grafen Sentezi ve Karakterizasyonu",
                description="CVD yöntemi ile grafen sentezi ve elektriksel özelliklerin incelenmesi",
                tags=["grafen", "CVD", "2D malzemeler"],
                created_by=users[1].id,
            ),
        ]
        for project in projects:
            session.add(project)
        session.commit()
        
        print(f"✅ {len(projects)} proje oluşturuldu")
        
        # Deneyler
        experiments = [
            Experiment(
                project_id=projects[0].id,
                title="77K Van der Pauw Ölçümleri",
                description="Sıvı azot sıcaklığında VDP yöntemi ile direnç ölçümleri",
                tags=["VDP", "77K", "direnç"],
            ),
            Experiment(
                project_id=projects[0].id,
                title="Hall Etkisi Ölçümleri",
                description="Değişken manyetik alan altında Hall katsayısı ölçümleri",
                tags=["Hall", "manyetik alan"],
            ),
            Experiment(
                project_id=projects[1].id,
                title="Raman Spektroskopisi",
                description="Grafen örneklerin Raman spektroskopisi ile karakterizasyonu",
                tags=["Raman", "spektroskopi"],
            ),
        ]
        for exp in experiments:
            session.add(exp)
        session.commit()
        
        print(f"✅ {len(experiments)} deney oluşturuldu")
        
        # Entry'ler
        entries = [
            Entry(
                experiment_id=experiments[0].id,
                author_id=users[0].id,
                title="Günlük - 2025-10-01",
                body_md="""## Deney Koşulları
- Sıcaklık: 77K (sıvı azot)
- Örnek: YBCO-01
- Kalınlık: ~200nm

## Ölçüm Sonuçları
Van der Pauw yöntemi ile 4-nokta direnç ölçümü yapıldı.

| Konfigürasyon | Direnç (Ω) |
|--------------|-----------|
| R12,34       | 12.5      |
| R23,41       | 11.8      |
| R34,12       | 12.2      |
| R41,23       | 12.0      |

## Notlar
- Örnekte homojen bir direnç dağılımı gözlendi
- Süperiletken geçiş sıcaklığı ~89K olarak belirlendi
""",
                tags=["VDP", "77K", "YBCO-01"],
            ),
            Entry(
                experiment_id=experiments[0].id,
                author_id=users[0].id,
                title="Günlük - 2025-10-03",
                body_md="""## Deney Koşulları
- Sıcaklık: 77K
- Örnek: YBCO-02
- Manyetik Alan: 0-1 Tesla

## Gözlemler
Farklı manyetik alan değerlerinde direnç ölçümleri tekrarlandı.
Manyetik alanla direnç artışı gözlendi (flux flow).

## Yapılacaklar
- [ ] Veri analizi tamamlanacak
- [ ] Grafik hazırlanacak
- [ ] Rapor yazılacak
""",
                tags=["VDP", "77K", "YBCO-02", "manyetik alan"],
            ),
        ]
        for entry in entries:
            session.add(entry)
        session.commit()
        
        print(f"✅ {len(entries)} entry oluşturuldu")
        
        # Şablonlar
        templates = [
            Template(
                type="docx",
                name="Standart Deney Raporu",
                description="Kurum standart DOCX şablonu",
                file_path="templates/report_v1.docx",
                is_default=True,
            ),
            Template(
                type="html",
                name="Basit PDF Şablonu",
                description="HTML bazlı basit rapor şablonu",
                file_path="templates/report_simple.html",
                is_default=False,
            ),
        ]
        for template in templates:
            session.add(template)
        session.commit()
        
        print(f"✅ {len(templates)} şablon kaydedildi")
        
        print("\n🎉 Örnek veriler başarıyla yüklendi!")
        print(f"   Kullanıcı: {users[0].email}")
        print(f"   Proje: {projects[0].name}")
        print(f"   Deney: {experiments[0].title}")
        print(f"   Entry: {entries[0].title}")


if __name__ == "__main__":
    seed_data()
