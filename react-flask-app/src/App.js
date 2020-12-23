import React, {useState, useEffect} from "react";
import logo from './logo.svg';
import './App.css';
import data from './data.json';
import ReactSearchBox from 'react-search-box'
import Select from "react-select";




class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {contacts: [],
      names : [],
      values : [],
      groupName: "",
      checked : false}
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);

    ;}

    handleChange(event) {
      this.setState({groupName: event.target.value});
    }
  
    handleSubmit(event) {
      alert('A name was submitted: ' + this.state.groupName);
      event.preventDefault();
      this.returnFlaskPost();
    }

  render() {
    return (
      <div className="App">
 < Contacts contacts = {this.state.contacts} />

     <Select
    isMulti
    onChange={this.onChange}
    options={this.state.contacts}
    value={this.state.values}
     
   />
   <p>
     <input
       onChange={this.onChangeCheckbox}
       type="checkbox"
       id="selectAll"
       value="selectAll"
       checked={this.state.checked}
     />
     <label for="selectAll">Select all</label>
   </p>

   <form onSubmit={this.handleSubmit}>
        <label>
          Group Name:  <br></br>
          <input type="text" groupName={this.state.groupName} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Save" />
      </form>



 


</div>

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
  onChangeCheckbox = e => {
    const isChecked = !this.state.checked;
    this.setState({
      checked: isChecked,
      values : isChecked ? this.state.contacts : this.state.values
    });
  };

  onChange = opt => {
    let allContactsvalues = (opt == null) ? 0 === this.state.contacts.length : opt.length === this.state.contacts.length;
    this.setState({
      checked : allContactsvalues ? true : false, 
      values : opt 
    });
  };


  returnFlaskPost = e => {
  const data = JSON.stringify({"groupName": this.state.groupName, "contacts" : this.state.values});
  console.log(data);
  return fetch( 'http://localhost:5000/fetch', {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }, 
    mode: 'cors',
    method: 'POST',
    body: data,
    }
  );
}

};



export default App;


function Contacts(props) {
  return (
  <div>
      <center><h1>Create a group</h1></center>
     <center> <table>
      <tr>
        <th> ID </th>
        <th> Name </th>
      </tr>
      {props.contacts.map((contact) => (
      <tr key={contact.id}>
          
          <td  class="card-title">{contact.value}</td>
          <td class="card-name">{contact.label}</td>
          
      </tr>
      ))}
      </table></center>
  </div>
  )
};

