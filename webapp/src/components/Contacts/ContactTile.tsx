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

const ContactTile = ({ id, member_id, number, name, created_on }: IContact) => {

  return (
    <Card sx={{ marginBottom: '12px' }} variant='outlined'>
      <CardContent>
        <Typography variant="h5" component="div">
          {phoneFormat(number!)}<DeleteIcon onClick={() => deleteContact(member_id!, number!)} sx={{ marginLeft: '12px' }} /><EditIcon sx={{ marginLeft: '12px' }} />
        </Typography>
        <Box style={{ marginTop: '16px' }}>
          {
            name &&
            <Chip color="primary" avatar={<Avatar>👤</Avatar>} label={contactNameFormat(name!)} />
          }
          <Typography variant="subtitle2" component="div" style={{ marginTop: '16px' }}>
            {createdOnDateFormat(created_on!)}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ContactTile; 
