export interface IContact {
    id: number;
    name: string;
    number: string;
    member_id: number;
    created_on: string;
};

export interface IMember {
    id: number;
    proxy_number: string;
    name: string;
    email: string;
    number: string;
    created_on: string;
};

export interface ContactProps {
    contact: IContact
};

export const addContact = (member_id: number, number: string, name: string | null) => {

    let headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append("Content-Type", "application/json");

    let raw = JSON.stringify({
        "number": number,
        "member_id": member_id,
        "name": name,
    });

    let options: RequestInit = {
        method: 'POST',
        headers: headers,
        body: raw,
        redirect: 'follow'
    };

    let url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/contacts`; 

    return fetch(url, options);
  
};

export const getContacts = (member_id: number) => {

    let headers = new Headers();
    headers.append('Accept', 'application/json');

    let queryParams = new URLSearchParams();
    queryParams.append('member_id', member_id.toString());

    let options: RequestInit = {
        method: 'GET',
        headers: headers,
        redirect: 'follow'
    };

    let url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/contacts?${queryParams}`; 

    return fetch(url, options);
  
};

export const deleteContact = (member_id: number, number: string) => {

    let headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append("Content-Type", "application/json");

    console.log(member_id)
    console.log(number)

    let raw = JSON.stringify({
        "number": number,
        "member_id": member_id,
    });

    let options: RequestInit = {
        method: 'DELETE',
        headers: headers,
        body: raw,
        redirect: 'follow'
    };

    let url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/contacts`; 

    return fetch(url, options);

}

export const getMember = (member_id: number) => {

    let headers = new Headers();
    headers.append('Accept', 'application/json');

    let queryParams = new URLSearchParams();
    queryParams.append('id', member_id.toString());

    let options: RequestInit = {
        method: 'GET',
        headers: headers,
        redirect: 'follow'
    };

    let url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/members?${queryParams}`; 

    return fetch(url, options);
  
};
