import get from 'lodash/get';

import {rootState} from '../store/reducers';

import {GENERAL_PATH} from "./reducer";

import {fields} from './enum';

import {layoutState} from './types';
import {SelectorListType} from "../components/SearchSelector/types";

const getStateData = (state: rootState): layoutState => get(state, GENERAL_PATH);
export const getFetching = (state: rootState): layoutState[fields.FETCHING] => get(getStateData(state), fields.FETCHING, {});
export const getFetchingComponent = (state: rootState): layoutState[fields.FETCHING] => get(getStateData(state), fields.FETCHING_COMPONENT, {});
export const getErrors = (state: rootState): layoutState[fields.ERRORS] => get(getStateData(state), fields.ERRORS, []);
export const getSuccessMessages = (state: rootState): layoutState[fields.SUCCESS_MESSAGES] => get(getStateData(state), fields.SUCCESS_MESSAGES, []);
export const getAuth = (state: rootState): layoutState[fields.IS_AUTH] => get(getStateData(state), fields.IS_AUTH, false);

export const getUsers = (state: rootState): layoutState[fields.USERS] => get(getStateData(state), fields.USERS, []);
export const getUsersForSelector = (state: rootState): layoutState[fields.USERS] => getUsers(state).map((user: any): SelectorListType => ({
    //@ts-ignore
    value: user.id,
    label: `${user['first_name']} ${user['last_name']}`,
}));

export const isFetching = (state: rootState) => {
    const fetching = getFetching(state);

    return Object.keys(fetching).some(key => fetching[key] === true);
};

export const isFetchingComponentByKey = (state: rootState, key: string) => {
    const fetching = getFetchingComponent(state);

    return fetching[key];
};
