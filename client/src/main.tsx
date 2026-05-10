import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router'
import Landing from './pages/Landing.tsx'
import Projects from './pages/Projects.tsx'
import CreateProject from './pages/CreateProject.tsx'
import ProjectDetail from './pages/ProjectDetail.tsx'
import './main.css'
import HeaderLayout from './layouts/HeaderLayout.tsx'
import AuthCallback from './pages/AuthCallback.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/auth/callback' element={<AuthCallback/>}/>
        <Route element={<HeaderLayout/>}>
          <Route path='/' element={<Landing/>}/>
          <Route path='/projects' element={<Projects/>}/>
          <Route path='/projects/new' element={<CreateProject/>}/>
          <Route path='/projects/:projectId' element={<ProjectDetail/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
