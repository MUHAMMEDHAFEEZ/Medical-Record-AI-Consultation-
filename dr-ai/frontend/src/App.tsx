import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import MedicalRecord from './components/MedicalRecord';
import PrivateRoute from './components/PrivateRoute';
import './App.css';
import DownloadRecord from './components/DownloadRecord';
import Record from './components/Record';


function App() {
  return (
    <Router>
      <Routes>
<      Route path="/record" element={<Record />} />
        <Route path="/login" element={<Login />} />
        <Route 
          path="/dashboard" 
          element={
            <PrivateRoute>
              <MedicalRecord />
            </PrivateRoute>
          } 
        />
        <Route path="/record/:id" element={<MedicalRecord />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />     
        <Route path="/downloadrecord/:id" element={<DownloadRecord />} />
      </Routes>
    </Router>
  );
}

export default App;



