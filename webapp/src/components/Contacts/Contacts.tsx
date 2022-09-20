import { useState, useEffect } from 'react'
import { styled } from '@mui/material/styles';
import Container from '@mui/material/Container';
import { getContacts, IMember, IContact } from '../../api/client';
import ContactTile from './ContactTile';

const Header = styled('h1')(({}) => ({
  color: 'white',
  marginTop: '24px',
  marginBottom: '16px',
}))

const Contacts = ({ id }: IMember) => {

  const [contacts, setContacts] = useState<IContact[]>([]);
  const [error, setError] = useState({});

  useEffect(() => {
    getContacts(id!)
      .then((response) => response.json())
      .then((data) => setContacts(data))
      .catch((error) => setError(error))
  }, [id]);

  console.log(error);
  console.log(contacts);

  return (
    <Container maxWidth="xl">
      <Header>Contacts</Header>
        <div style={{ height: 400, width: '100%' }}>
          {
            contacts.map((contact) =>
              <ContactTile id={contact.id} number={contact.number} name={contact.name} />
            )
          }
        </div>
    </Container>
  );

};

export default Contacts;
