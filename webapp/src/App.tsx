import { useState, useEffect } from 'react'
import './App.css';

interface Contact {
  id: number;
  name: string;
  number: string;
  memberId: number;
  createdOn: string;
}

function getContacts(memberId: number) {

  const headers = new Headers();
  headers.append("Accept", "application/json");
  
  const options: RequestInit = {
    method: 'GET',
    headers: headers,
    redirect: 'follow'
  };

  const base = 'https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/contacts?'
  const queryParams = new URLSearchParams();
  queryParams.append('member_id', memberId.toString());

  const url = base + queryParams;  
  const result = fetch(url, options);
  return result;
}


function App() {

  const [contacts, setContacts] = useState<Contact[]>([]);
  const [error, setError] = useState({});

  useEffect(() => {
    getContacts(3)
    .then((response) => console.log(response))
    // .then((data) => console.log('hi'))
    // .catch((error) => setError(error))
  }, []);

  // console.log(error);
  // console.log(contacts);

  return (
    <div className="App">
    </div>
  );
}

export default App;