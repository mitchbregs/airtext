import { useState, useEffect } from 'react'
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import { addContact, getContacts, IContact, IMember } from '../../api/client';
import ContactTile from './ContactTile';
import Stack from '@mui/material/Stack';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

const Header = styled('h1')(({ }) => ({
  color: 'black',
  marginTop: '24px',
  marginBottom: '16px',
}))

interface MemberProps {
  member: IMember;
}

const boxStyle = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '60%',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const Contacts = (props: MemberProps) => {

  const [contacts, setContacts] = useState<IContact[]>([]);
  const [error, setError] = useState({});

  const [nameInput, setNameInput] = useState<string>('');
  const [numberInput, setNumberInput] = useState<string>('');

  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  function allContacts(member_id: number) {
    getContacts(member_id)
      .then(response => response.json())
      .then(data => setContacts(data))
      .catch(error => setError(error))
  } 

  function removeContact(id: number | undefined) {
    setContacts(contacts.filter(c => c.id !== id))
  }

  function appendContact(contact: object) {
    setContacts([ ...contacts, contact as IContact]);
    setNumberInput('');
    setNameInput('');
  }

  function createContact(member_id: number) {
    let number = numberInput === '' ? null : numberInput
    let name = nameInput === '' ? null : nameInput
    addContact(member_id, number!, name)
      .then(response => {
        if (response.status === 200) {
          return response.json()
        } else {
          throw response.json()
        }
      })
      .then(data => appendContact(data))
      .catch(error => setError(error))
    handleClose()
  }

  useEffect(() => {
    allContacts(props.member.id)
  }, [props.member.id]);

  return (
    <Container maxWidth="xl">
      <Stack spacing={2} direction="row">
        <Header>Contacts</Header>
        <Button variant="contained" color="primary" onClick={handleOpen}>Create</Button>
      </Stack>
      <div style={{ height: 400, width: '100%' }}>
        {
          contacts.map((contact, index) =>
            <ContactTile
              key={`ContactTile-${index}`}
              contact={contact}
              stateChange={removeContact}
            />
          )
        }
      </div>
      <Modal
        open={open}
        onClose={handleClose}
      >
        <Box sx={boxStyle}>
          <Stack
            component="form"
            spacing={2}
            noValidate
            autoComplete="off"
          >
            <TextField
              hiddenLabel
              required
              id="number"
              value={numberInput}
              placeholder="Number"
              variant="filled"
              onChange={e => setNumberInput(e.target.value!)}
            />
            <TextField
              hiddenLabel
              id="name"
              value={nameInput}
              placeholder="Name"
              variant="filled"
              onChange={e => setNameInput(e.target.value)}
            />
            <Button
              onClick={() => createContact(props.member.id)}
            >Create</Button>
          </Stack>
        </Box>
      </Modal>
    </Container>
  );

};

export default Contacts;
