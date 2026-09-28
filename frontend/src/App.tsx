import { useState, useEffect, useMemo } from 'react';
import './index.css';

interface Subject {
  name: string;
  credit: number;
  grade: number;
}

function App() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [semesters, setSemesters] = useState<any[]>([]);
  const [selectedSemester, setSelectedSemester] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [telegramId, setTelegramId] = useState<string | null>(null);

  const API_BASE = "http://127.0.0.1:8000/api/v1";

  // URL'dan Telegram ID'ni olish (Mini App orqali)
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tgId = params.get('user_id');
    if (tgId) setTelegramId(tgId);
    else setTelegramId("5139310978"); // Test uchun ID (siz yuborgan datadan)
  }, []);

  useEffect(() => {
    if (telegramId) fetchSemesters();
  }, [telegramId]);

  const fetchSemesters = async () => {
    try {
      const res = await fetch(`${API_BASE}/hemis/semesters/${telegramId}`);
      if(res.ok) {
        const data = await res.json();
        if(data.data && data.data.items) {
          setSemesters(data.data.items);
          if (data.data.items.length > 0) setSelectedSemester(data.data.items[0].code);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (selectedSemester && telegramId) fetchSubjects();
  }, [selectedSemester, telegramId]);

  const fetchSubjects = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/hemis/subjects/${telegramId}?semester_id=${selectedSemester}`);
      if(res.ok) {
        const data = await res.json();
        if(data.data && data.data.items) {
          const parsed = data.data.items.map((item: any) => ({
             name: item.subject?.name || item.name || "Noma'lum fan",
             credit: parseFloat(item.credit || "0"),
             grade: parseInt(item.grade || item.rating || "0")
          }));
          setSubjects(parsed);
        }
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleGradeChange = (index: number, newGrade: number) => {
    const newSubjects = [...subjects];
    newSubjects[index].grade = newGrade;
    setSubjects(newSubjects);
  };

  const gpa = useMemo(() => {
    let totalCredits = 0;
    let totalScore = 0;
    subjects.forEach(sub => {
      if (sub.grade > 0 && sub.credit > 0) {
         totalCredits += sub.credit;
         totalScore += sub.grade * sub.credit;
      }
    });
    if (totalCredits === 0) return (0).toFixed(2);
    return (totalScore / totalCredits).toFixed(2);
  }, [subjects]);

  return (
    <>
      <div className="floating-header">
        <div style={{fontWeight: 700}}>O'zMU GPA</div>
        <div className="gpa-display">{gpa} GPA</div>
      </div>

      <div className="container">
        <select 
          className="glass-select" 
          value={selectedSemester} 
          onChange={e => setSelectedSemester(e.target.value)}
        >
          {semesters.map(sem => (
            <option key={sem.code} value={sem.code}>{sem.name}</option>
          ))}
        </select>

        {loading ? <div className="loader"></div> : (
          <div>
            {subjects.map((sub, index) => (
              <div key={index} className="subject-card" style={{animationDelay: `${index * 0.05}s`}}>
                <div className="subject-header">
                  <h3 className="subject-title">{sub.name}</h3>
                  <span className="subject-credits">{sub.credit} Kredit</span>
                </div>
                <div className="grade-buttons">
                  {[2, 3, 4, 5].map(g => (
                    <button 
                      key={g} 
                      className={`grade-btn grade-${g} ${sub.grade === g ? 'active' : ''}`}
                      onClick={() => handleGradeChange(index, g)}
                    >
                      {g}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="floating-footer">
        <div style={{color: 'var(--text-muted)', fontSize: '0.9rem'}}>
          Baholarni o'zgartirib GPA ni hisoblang
        </div>
      </div>
    </>
  );
}

export default App;
