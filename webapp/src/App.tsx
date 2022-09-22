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

const airtextMember: IMember = {
  id: 3,
  proxy_number: "+19738745273",
  name: "mitchbregs",
  email: "mitch@mitchbregs.com",
  number: "+19086162014",
  created_on: "2022-08-12 20:02:57.085953"
}

const App = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <div className='App'>
        <Navigation member={airtextMember} />
        <Contacts member={airtextMember} />
      </div>
    </ThemeProvider>
  );
}

export default App;
