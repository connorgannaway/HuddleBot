<script setup>
import axios from 'axios';
import { onMounted } from 'vue';
import {ref} from 'vue'

const props = defineProps({
    jiratoken: String,
    id: String
})

var issue = {}
const summary = ref()
const callSuccess = ref(false)
const link = ref()
const issuetype = ref()
const description = ref()

//fetch jira issue data using passed id and token vars
function fetchIssueData(){
    axios.get(
        `https://api.atlassian.com/ex/jira/${import.meta.env.VITE_CLOUD_ID}/rest/api/3/issue/${props.id}`,
        {headers: {
            Authorization: `Bearer ${props.jiratoken}`
        }}
    )
    .then((res) => {
        //console.log(res.data)
        issue = res.data
        splitData()
    })
    .catch((err) => {
        console.log(err)
    })
}

//split response data into variables for easy access
function splitData(){
    summary.value = issue.fields.summary
    link.value = `https://cgannaway.atlassian.net/browse/${props.id}`
    issuetype.value = issue.fields.issuetype.name

    try{
        description.value = issue.fields.description.content['0'].content['0'].text
        if(description.value.length > 150){
            description.value = description.value.substring(0, 150) + "..."
        }
    }
    catch{}

    callSuccess.value = true

}

//open issue in new tab
function openIssue(){
    window.open(link.value)
}

onMounted(() => {
    fetchIssueData()
})

</script>

<template>
    <div class="issue">
        <div v-if="callSuccess" @click="openIssue">
            <div class="title">
                <h2>{{summary}}</h2>
            </div>
            <div class="desc">
                <p>{{description}}</p>
            </div>
            <div class="info">
                <div class="statusicon">
                    <small>
                        <img src="../assets/bug.svg" height="18" v-if="issuetype=='Bug'" />
                        <img src="../assets/epic.svg" height="18" v-if="issuetype=='Epic'" />
                        <img src="../assets/improvement.svg" height="18" v-if="issuetype=='Improvement'" />
                        <img src="../assets/story.svg" height="18" v-if="issuetype=='Story'" />
                        <img src="../assets/task.svg" height="18" v-if="issuetype=='Task'" />
                        <img src="../assets/datafix.png" height="18" v-if="issuetype=='Data Fix'" />
                        {{id}}</small>
                </div>
            </div>
        </div>
        <div v-if="callSuccess==false">
            <p>loading...</p>
        </div>
    </div>
</template>

<style scoped>
.issue {
    text-align: left;
    padding: 10px;
    padding-left: 30px;
    border-radius: 10px;
    background: white;
    max-width: 400px;
    min-width: 25vw;
    margin-bottom: 20px;
}
.statusicon {
    height: 20px;
    line-height: 15px;
    text-align: left;
    margin: auto;
    
}
.statusicon img{
    margin-right: 10px;
}
.desc {
    margin-bottom: 15px;
}

</style>
