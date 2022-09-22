import { CardHeader, Icon } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Chip from '@mui/material/Chip';
import Typography from '@mui/material/Typography';
import { IContact, deleteContact } from '../../api/client'
import { contactNameFormat, createdOnDateFormat, phoneFormat } from '../../api/helpers';

interface ContactTileProps {
  contact: IContact;
  stateChange: Function,
}

const ContactTile = (props: ContactTileProps) => {

  function runDeleteContact(contact_id: number, member_id: number, number: string, stateChange: Function) {
    deleteContact(member_id, number)
      .then(response => response.json())
      .then(data => stateChange(contact_id))
      .catch(error => console.log(error));
  }

  return (
    <Card sx={{ marginBottom: '12px' }} variant='outlined'>
      <CardContent>
        <Typography variant="h5" component="div">
          {phoneFormat(props.contact.number)}<DeleteIcon onClick={() => runDeleteContact(props.contact.id, props.contact.member_id, props.contact.number, props.stateChange)} sx={{ marginLeft: '12px' }} /><EditIcon sx={{ marginLeft: '12px' }} />
        </Typography>
        <Box style={{ marginTop: '16px' }}>
          {
            props.contact.name &&
            <Chip color="primary" avatar={<Avatar>👤</Avatar>} label={contactNameFormat(props.contact.name)} />
          }
          <Typography variant="subtitle2" component="div" style={{ marginTop: '16px' }}>
            {createdOnDateFormat(props.contact.created_on)}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ContactTile; 
