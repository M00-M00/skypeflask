import React, {useState, useEffect} from "react";
import logo from './logo.svg';
import './App.css';
import data from './data.json';
import ReactSearchBox from 'react-search-box'




class App extends React.Component {
  state = {
    contacts: []
  };
  render() {
    return (
     < Contacts contacts = {this.state.contacts} />
    )
  }
  componentDidMount() {
    fetch(`/contacts`)
    .then(res => res.json())
    .then(data => {
    this.setState({ contacts: data.contact });
  })
  .catch(console.log);
}
}
const Contacts = ({ contacts }) => {
  return (
  <div>
      <center><h1>Contact List</h1></center>
     <center> <table>
      <tr>
        <th> ID </th>
        <th> Name </th>
      </tr>
      {contacts.map((contact) => (
      <tr>
          
          <td class="card-title">{contact.id}</td>
          <td class="card-name">{contact.name}</td>
          
      </tr>
      ))}
      </table></center>
  </div>
  )
};

export default App;
