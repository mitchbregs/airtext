export interface IContact {
    id?: number;
    name?: string;
    number?: string;
    member_id?: number;
    created_on?: string;
};

export interface IMember {
    id?: number;
    proxy_number?: string;
    name?: string;
    email?: string;
    number?: string;
    created_on?: string;
};

export const deleteContact = (memberId: number, number: string ) => {

    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append("Content-Type", "application/json");

    const raw = JSON.stringify({
        "member_id": memberId,
        "number": number
    });

    const options: RequestInit = {
        method: 'DELETE',
        headers: headers,
        body: raw,
        redirect: 'follow'
    };

    const url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/contacts`; 

    return fetch(url, options);

}

export const getContacts = (memberId: number) => {

    const headers = new Headers();
    headers.append('Accept', 'application/json');

    const queryParams = new URLSearchParams();
    queryParams.append('member_id', memberId.toString());

    const options: RequestInit = {
        method: 'GET',
        headers: headers,
        redirect: 'follow'
    };

    const url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/contacts?${queryParams}`; 

    return fetch(url, options);
  
};

export const getMember = (memberId: number) => {

    const headers = new Headers();
    headers.append('Accept', 'application/json');

    const queryParams = new URLSearchParams();
    queryParams.append('id', memberId.toString());

    const options: RequestInit = {
        method: 'GET',
        headers: headers,
        redirect: 'follow'
    };

    const url = `https://z4muss792f.execute-api.us-east-1.amazonaws.com/v1/members?${queryParams}`; 

    return fetch(url, options);
  
};