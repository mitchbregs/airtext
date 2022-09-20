import { ThemeProvider, createTheme } from '@mui/material/styles';
import './App.css';
import Contacts from './components/Contacts/Contacts'
import Navigation from './components/Utils/Navigation'
import { IMember } from './api/client';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const member: IMember = {
  id: 3
}

const App = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <div className='App'>
        <Navigation id={member.id} />
        <Contacts id={member.id} />
      </div>
    </ThemeProvider>
  );
}

export default App;
