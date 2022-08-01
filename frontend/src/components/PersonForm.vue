<script setup>
    import {onMounted, ref} from 'vue'
    import axios from 'axios'

    const first_name = ref()
    const last_name = ref()
    const slack_id = ref()
    const jira_id = ref()
    const start_date = ref()
    const end_date = ref()
    const is_active = ref(true)
    let slack_token = ''
    let jira_token = ''
    const slackmatchFound = ref(false)
    const slackattemptMatch = ref(false)
    const jiramatchFound = ref(false)
    const jiraattemptMatch = ref(false)
    const postCode = ref()

    
    function getTokens(){
        axios.get(
            'http://localhost:8000/api/token/?service=slack'
        )
        .then((res) => {
            slack_token = res.data.token
        })
        .catch((err) => {
            console.log(err)
        })

        axios.get(
            'http://localhost:8000/api/token/?service=jira'
        )
        .then((res) => {
            jira_token = res.data.token
        })
        .catch((err) => {
            console.log(err)
        })
    }

    function findSlackMatch(){
       // e.preventDefault()

        let body = `token=${slack_token}&limit=200`
        axios.post('https://slack.com/api/users.list', body)
        .then((res) => {
            console.log(res)
            let members = res.data.members
            for(const member of members){
                if(member.real_name == `${first_name.value} ${last_name.value}`){
                    slack_id.value = member.id
                    slackmatchFound.value = true
                }
            } 
//            if(slackmatchFound.value == false && res.data.response_metadata.next_cursor){
  //              let next = res.data.response_metadata.next_cursor
    //            console.log(next)
      //          let nextarr = next.split('')
        //        for(let i = 0; i < nextarr.length; i++){
          //          if(nextarr[i] == '='){
            //            nextarr.splice(i, 0, "%3D")
              //      }
                //}
        //        next = nextarr.join('')
          //      getNextSlackPage(next)
            //}

            slackattemptMatch.value = true
        })
        .catch((err) => {
            console.log(err)
        })
    }

    function getNextSlackPage(cursor){
        let body = `token=${slack_token}&limit=2&cursor=${next_cursor}`
        console.log(cursor)

        axios.post('https://slack.com/api/users.list', body)
        .then((res) => {
            console.log(res)
            let members = res.data.members
            for(const member of members){
                if(member.real_name == `${first_name.value} ${last_name.value}`){
                    slack_id.value = member.id
                    slackmatchFound.value = true
                }
            } 
            
            if(slackmatchFound.value == false && res.data.response_metadata.next_cursor){
                let cursor = res.data.response_metadata.next_cursor
                let cursorarr = cursor.split('')
                for(let i = 0; i < cursorarr.length; i++){
                    if(cursorarr[i] == '='){
                        cursorarr.splice(i, 0, "%3D")
                    }
                }
                cursor = cursorarr.join('')
                getNextSlackPage(cursor)
            }
        })
        .catch((err) => {
            console.log(err)
        })
    }

    function findJiraMatch(e){
        e.preventDefault()
        let config = {
            params: {
                maxResults: 200
            },
            headers: {
                Authorization : `Bearer ${jira_token}`
            }
        }

        axios.get(
            `https://api.atlassian.com/ex/jira/${import.meta.env.VITE_CLOUD_ID}/rest/api/3/users/search`,
            config
        )
        .then((res) => {
            for(const user of res.data){
                if(user.displayName == `${first_name.value} ${last_name.value}`){
                    jiramatchFound.value = true
                    jira_id.value = user.accountId
                }
            }
            jiraattemptMatch.value = true
        })
    }

    function sumbitForm(e){
        e.preventDefault()
        
        if(end_date.value == ''){
            end_date.value = null
        }
        
        let params = {
            first_name: first_name.value,
            last_name: last_name.value,
            slack_id: slack_id.value,
            jira_id: jira_id.value,
            start_date: start_date.value,
            end_date: end_date.value,
            is_active: is_active.value
        }
    

        axios.post(
            'http://localhost:8000/api/person/',
            params
        )
        .then((res) => {
            console.log(res)
            postCode.value = res.status
        })
        .catch((err) => {
            console.log(err)
            postCode.value = err.response.status
        })
    }
    
    
    onMounted(() => {
        getTokens()
    })

</script>



<template>

    <form>
        <h1>Create Person</h1>
        <label>First Name</label>
        <input v-model="first_name" />

        <label>Last Name</label>
        <input v-model="last_name" />
        <label>Slack ID - 
            <button @click="findSlackMatch" @click.prevent="submit">Search</button> 
            <p v-if="slackmatchFound && slackattemptMatch" class="success">Match Found</p> 
            <p v-if="slackattemptMatch && !slackmatchFound" class="error">No Match Found</p>
        </label>
        <input v-model="slack_id" />

        <label>Jira ID - 
            <button @click="findJiraMatch">Search</button> 
            <p v-if="jiramatchFound && jiraattemptMatch" class="success">Match Found</p> 
            <p v-if="jiraattemptMatch && !jiramatchFound" class="error">No Match Found</p>
        </label>
        <input v-model="jira_id" />

        <label>Start Date</label>
        <input type="date" v-model="start_date" />

        <label>End Date</label>
        <input type="date" v-model="end_date" />

        <label>Active</label>
        <input type="checkbox" v-model="is_active" />
        <button @click="sumbitForm">Submit</button>
        <p v-if="postCode == 201" class="success">Object Created</p>
        <p v-if="postCode == 400" class="error">Error. (Make sure Slack/Jira ID fields are unique!)</p>
    </form>

</template>

<style scoped>
    h1 {
        font-weight: 400;
    }
    form {
        text-align: left;
        padding: 30px;
        border-radius: 10px;
        background: white;
        max-width: 400px;
        min-width: 25vw;
    }
    label {
        display: inline-block;
        margin: 10px 0 5px;
        font-size: 1rem;
        text-transform: uppercase;
        font-weight: normal;

    }
    input {
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 2px solid #ddd;
    }
    .success {
        color:green;
    }
    .error {
        color: red;
    }
</style>
