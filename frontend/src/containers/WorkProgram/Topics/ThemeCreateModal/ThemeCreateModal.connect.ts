import {Dispatch} from "react";
import {connect} from 'react-redux';
import {bindActionCreators} from "redux";

import {rootState} from "../../../../store/reducers";

import actions from "../../actions";
import {getAllSectionsForSelect, isOpenDialog, getDialogData} from '../../getters';
import {WorkProgramActions} from "../../types";
import {fields} from "../../enum";

import coursesActions from '../../../Courses/actions';
import {CoursesActions} from '../../../Courses/types';
import {getCoursesForSelector} from "../../../Courses/getters";

const mapStateToProps = (state: rootState) => {
    return {
        coursesList: getCoursesForSelector(state),
        sections: getAllSectionsForSelect(state),
        isOpen: isOpenDialog(state, fields.CREATE_NEW_TOPIC_DIALOG),
        topic: getDialogData(state, fields.CREATE_NEW_TOPIC_DIALOG),
    };
};

const mapDispatchToProps = (dispatch: Dispatch<WorkProgramActions|CoursesActions>) => ({
    // @ts-ignore
    actions: bindActionCreators(actions, dispatch),
    // @ts-ignore
    coursesActions: bindActionCreators(coursesActions, dispatch),
});

// @ts-ignore
export default connect(mapStateToProps, mapDispatchToProps);
