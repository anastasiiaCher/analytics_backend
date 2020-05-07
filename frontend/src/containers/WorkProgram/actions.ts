import {createAction} from "@reduxjs/toolkit";

import {WorkProgramActions} from './types';

const getWorkProgram = createAction<string>('GET_WORK_PROGRAM');
const setWorkProgram = createAction<string>('SET_WORK_PROGRAM');
const setWorkProgramId = createAction<string>('SET_WORK_PROGRAM_ID');
const saveWorkProgram = createAction<string>('SAVE_WORK_PROGRAM');
const setWorkProgramPart = createAction<string>('SET_WORK_PROGRAM_PART');

const saveSection = createAction<string>('SAVE_SECTION');
const deleteSection = createAction<string>('DELETE_SECTION');
const changeSectionNumber = createAction<string>('CHANGE_SECTION_NUMBER');

const actions: WorkProgramActions = {
    getWorkProgram,
    setWorkProgram,
    setWorkProgramId,
    setWorkProgramPart,
    saveWorkProgram,
    saveSection,
    deleteSection,
    changeSectionNumber,
}

export default actions;
