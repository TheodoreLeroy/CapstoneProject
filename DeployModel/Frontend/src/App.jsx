import { BrowserRouter, Route, Routes } from "react-router-dom"
import Login from "./pages/Login"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import Register from "./pages/Register"
import Attendent from "./pages/Attendent"
import NewClass from "./pages/NewClass"
import NewSlot from "./pages/NewSlot"

  function App() {

    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login></Login>} />
          <Route path="/register" element={<Register></Register>} />
          <Route path="/home" element={<Home />} />
          <Route path="/class/:id" element={<NewSlot /> }>
            <Route path="slot=:id"/>
          </Route>
          <Route path="/attendent" element={<Attendent />}>
            <Route path=":class/:subject" element={<Attendent />} />
          </Route>
          <Route path="/newClass" element={<NewClass />} />
          <Route path="*" element={<NotFound></NotFound>}></Route>
        </Routes>
      </BrowserRouter>
    )
  }

export default App
