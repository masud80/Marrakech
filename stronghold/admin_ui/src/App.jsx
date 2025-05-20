import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import AssetInventory from './pages/AssetInventory';
import MLModelStatus from './pages/MLModelStatus';
import DataIngestion from './pages/DataIngestion';
import Settings from './pages/Settings';
import { Box } from '@mui/material';
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f4f6f8' }}>
        <Sidebar />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Routes>
            <Route path="/" element={<Navigate to="/assets" replace />} />
            <Route path="/assets" element={<AssetInventory />} />
            <Route path="/ml-models" element={<MLModelStatus />} />
            <Route path="/data-ingestion" element={<DataIngestion />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  )
}

export default App
