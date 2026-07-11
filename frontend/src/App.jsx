import { useState } from 'react'
import './App.css'

function App() {
  // Form states
  const [gender, setGender] = useState('female')
  const [raceEthnicity, setRaceEthnicity] = useState('group B')
  const [parentalEducation, setParentalEducation] = useState('some college')
  const [lunch, setLunch] = useState('standard')
  const [testPrep, setTestPrep] = useState('none')
  const [readingScore, setReadingScore] = useState(70)
  const [writingScore, setWritingScore] = useState(70)

  // System states
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [usingMock, setUsingMock] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setUsingMock(false)

    // Form client-side validation
    const readVal = Number(readingScore)
    const writeVal = Number(writingScore)
    if (isNaN(readVal) || readVal < 0 || readVal > 100 || isNaN(writeVal) || writeVal < 0 || writeVal > 100) {
      setError('Scores must be integers between 0 and 100.')
      setLoading(false)
      return
    }

    const payload = {
      gender,
      race_ethnicity: raceEthnicity,
      parental_level_of_education: parentalEducation,
      lunch,
      test_preparation_course: testPrep,
      reading_score: readVal.toString(),
      writing_score: writeVal.toString()
    }

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`Server status ${response.status}`)
      }

      const data = await response.json()
      if (data && typeof data.results !== 'undefined') {
        // Ensure result is formatted to at most 2 decimal places if it's a float
        const score = typeof data.results === 'number' ? Math.round(data.results * 10) / 10 : data.results
        setResult(score)
      } else {
        throw new Error('Invalid JSON format from backend')
      }
    } catch (err) {
      console.warn('Could not fetch prediction from backend, using client-side mock predictor:', err)
      
      // Sophisticated local mock calculation representing the student performance dataset relationships
      let mockScore = Math.round(
        readVal * 0.55 +
        writeVal * 0.35 +
        (gender === 'male' ? 3.5 : 0) + // In this dataset, males score slightly higher on average in math
        (testPrep === 'completed' ? 4.5 : -1.5) +
        (lunch === 'standard' ? 3.0 : -2.0) +
        (raceEthnicity === 'group E' ? 4.0 : raceEthnicity === 'group D' ? 2.0 : -1.0)
      )
      mockScore = Math.min(100, Math.max(0, mockScore))

      // Simulate a small network latency for natural UX flow
      await new Promise((resolve) => setTimeout(resolve, 800))
      setResult(mockScore)
      setUsingMock(true)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setUsingMock(false)
    setError(null)
  }

  // Helper to determine the rating color/label based on math score
  const getRating = (score) => {
    const s = Number(score)
    if (s >= 85) return { label: 'Excellent', color: '#10b981' } // green
    if (s >= 70) return { label: 'Good', color: '#84cc16' }      // lime
    if (s >= 50) return { label: 'Average', color: '#f59e0b' }   // amber
    return { label: 'Needs Improvement', color: '#ef4444' }     // red
  }

  const rating = result !== null ? getRating(result) : null

  return (
    <div className="app-container">
      <header className="header">
        <h1 className="header-title">Student Score Predictor</h1>
        <p className="header-subtitle">
          Input student demographic and performance characteristics to estimate their final Mathematics exam score.
        </p>
      </header>

      <div className="prediction-card">
        {usingMock && (
          <div className="alert alert-warning">
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <span className="badge badge-warning">Demo Mode</span> Flask backend is offline or unreachable. Displaying local prediction.
            </div>
          </div>
        )}

        {error && (
          <div className="alert alert-error">
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {result === null ? (
          <form className="prediction-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              
              <div className="input-group">
                <label className="input-label" htmlFor="gender">Gender</label>
                <select
                  id="gender"
                  className="input-control"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                >
                  <option value="female">Female</option>
                  <option value="male">Male</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label" htmlFor="race">Race / Ethnicity</label>
                <select
                  id="race"
                  className="input-control"
                  value={raceEthnicity}
                  onChange={(e) => setRaceEthnicity(e.target.value)}
                >
                  <option value="group A">Group A</option>
                  <option value="group B">Group B</option>
                  <option value="group C">Group C</option>
                  <option value="group D">Group D</option>
                  <option value="group E">Group E</option>
                </select>
              </div>

              <div className="input-group full-width">
                <label className="input-label" htmlFor="parentEducation">Parental Education Level</label>
                <select
                  id="parentEducation"
                  className="input-control"
                  value={parentalEducation}
                  onChange={(e) => setParentalEducation(e.target.value)}
                >
                  <option value="some high school">Some High School</option>
                  <option value="high school">High School</option>
                  <option value="some college">Some College</option>
                  <option value="associate's degree">Associate's Degree</option>
                  <option value="bachelor's degree">Bachelor's Degree</option>
                  <option value="master's degree">Master's Degree</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label" htmlFor="lunch">Lunch Program</label>
                <select
                  id="lunch"
                  className="input-control"
                  value={lunch}
                  onChange={(e) => setLunch(e.target.value)}
                >
                  <option value="standard">Standard</option>
                  <option value="free/reduced">Free / Reduced</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label" htmlFor="testPrep">Test Prep Course</label>
                <select
                  id="testPrep"
                  className="input-control"
                  value={testPrep}
                  onChange={(e) => setTestPrep(e.target.value)}
                >
                  <option value="none">None</option>
                  <option value="completed">Completed</option>
                </select>
              </div>

              <div className="input-group">
                <label className="input-label" htmlFor="readingScore">
                  <span>Reading Score</span>
                  <span>{readingScore}/100</span>
                </label>
                <input
                  id="readingScore"
                  type="range"
                  min="0"
                  max="100"
                  className="input-control"
                  value={readingScore}
                  onChange={(e) => setReadingScore(Number(e.target.value))}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label" htmlFor="writingScore">
                  <span>Writing Score</span>
                  <span>{writingScore}/100</span>
                </label>
                <input
                  id="writingScore"
                  type="range"
                  min="0"
                  max="100"
                  className="input-control"
                  value={writingScore}
                  onChange={(e) => setWritingScore(Number(e.target.value))}
                  required
                />
              </div>

            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Processing Prediction...
                </>
              ) : (
                'Predict Mathematics Score'
              )}
            </button>
          </form>
        ) : (
          <div className="result-container">
            <div className="result-glow" style={{ borderColor: rating.color, boxShadow: `0 0 35px ${rating.color}44` }}>
              <div className="result-score" style={{ color: rating.color }}>{result}</div>
            </div>
            <h2 className="result-title">Predicted Math Score</h2>
            <p className="result-description">
              Based on the provided demographic attributes, reading score ({readingScore}/100), and writing score ({writingScore}/100), the student is predicted to achieve a math grade of <strong>{result}%</strong>, categorizing their performance as <strong>{rating.label}</strong>.
            </p>
            <button className="secondary-btn" onClick={handleReset}>
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
              </svg>
              Make Another Prediction
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
