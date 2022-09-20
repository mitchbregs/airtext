import Avatar from '@mui/material/Avatar';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { isNamedExports } from 'typescript';
import { IContact } from '../../api/client'
import { phoneFormat } from '../../api/helpers';

const ContactTile = ({ id, number, name }: IContact) => {

  return (
    <Card sx={{ minWidth: 275, marginBottom: '12px' }} variant='outlined'>
      <CardContent>
        <Stack direction="row" spacing={1}>
          <Typography variant="h6" component="div">
          {phoneFormat(number!)}
          </Typography>
          {name && <Chip color="default" avatar={<Avatar>@</Avatar>} label={name} />}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ContactTile; 
