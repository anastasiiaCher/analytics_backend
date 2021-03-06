import React from 'react';
import get from 'lodash/get';
import Scrollbars from "react-custom-scrollbars";

import {SortableContainer, SortableElement, SortableHandle} from 'react-sortable-hoc';

import TableContainer from "@material-ui/core/TableContainer";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";

import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import withStyles from '@material-ui/core/styles/withStyles';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';

import EditedRow from "./EditedRow";

import {SecondStepProps} from './types';
import {workProgramSectionFields} from "../enum";

import connect from './Sections.connect';
import styles from './Sections.styles';

class Sections extends React.PureComponent<SecondStepProps> {
    scrollBar: any = null;

    state = {
        createNewSectionMode: false
    }

    getNewSection = () => ({
        name: '',
        SRO: '',
        contact_work: '',
        lecture_classes: '',
        practical_lessons: '',
        total_hours: '',
        laboratory: '',
        ordinal_number: get(this, 'props.sections.length', 0) + 1 ,
    })

    handleCreateNewSection = () => {
        this.setState({
            createNewSectionMode: true,
        });
        this.scrollBar.scrollToBottom();
    };

    removeNewSection = () => {
        this.setState({
            createNewSectionMode: false,
        });
    }

    onSortEnd = ({oldIndex, newIndex}: any) => {
        const {sections} = this.props;

        this.props.actions.changeSectionNumber({sectionId: sections[oldIndex].id, newNumber: newIndex + 1});
    }

    getTotalHours = (field: string) => {
        const {sections} = this.props;

        let count = 0;

        sections.forEach(section => {
            //@ts-ignore
            count += Boolean(section[field]) ? parseFloat(section[field]) : 0;
        })

        return count;
    };

    render() {
        const {classes, sections, isCanEdit} = this.props;
        const {createNewSectionMode} = this.state;

        const totalLectureClassesHours = this.getTotalHours(workProgramSectionFields.LECTURE_CLASSES).toFixed(2);
        const totalLaboratoryClassesHours = this.getTotalHours(workProgramSectionFields.LABORATORY).toFixed(2);
        const totalPracticalClassesHours = this.getTotalHours(workProgramSectionFields.PRACTICAL_LESSONS).toFixed(2);
        const totalSPOHours = this.getTotalHours(workProgramSectionFields.SPO).toFixed(2);

        const totalContactWorkHours = ((
            parseFloat(totalLectureClassesHours) +
            parseFloat(totalLaboratoryClassesHours) +
            parseFloat(totalPracticalClassesHours))
            * 1.1).toFixed(2);

        const totalTotalHours = (parseFloat(totalSPOHours) + parseFloat(totalContactWorkHours)).toFixed(2);

        return (
            <div className={classes.secondStep}>
                <TableContainer className={classes.table}>
                    <Scrollbars ref={(el) => {this.scrollBar = el}}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell className={classes.headerCell} rowSpan={2} colSpan={isCanEdit ? 2 : 1}> № раздела </TableCell>
                                    <TableCell className={classes.headerCell} rowSpan={2}>Наименование раздела дисциплины</TableCell>
                                    <TableCell className={classes.headerCell} colSpan={isCanEdit ? 6 : 5}>Распределение часов по дисциплине</TableCell>
                                    <TableCell className={classes.headerCell} rowSpan={isCanEdit ? 2 : 1}> </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell className={classes.headerCell}>Контактная работа</TableCell>
                                    <TableCell className={classes.headerCell}>Занятия лекционного типа</TableCell>
                                    <TableCell className={classes.headerCell}>Лабораторные занятия</TableCell>
                                    <TableCell className={classes.headerCell}>Практические занятия</TableCell>
                                    <TableCell className={classes.headerCell}>СРО</TableCell>
                                    <TableCell className={classes.headerCell}>Всего часов</TableCell>
                                </TableRow>
                            </TableHead>

                            <SortableList sections={sections}
                                          useDragHandle={true}
                                          hideSortableGhost={false}
                                          removeNewSection={this.removeNewSection}
                                          onSortEnd={this.onSortEnd}
                                          isCanEdit={isCanEdit}
                            />

                            {createNewSectionMode &&
                                <TableRow>
                                    <TableCell style={{border: '1px solid rgba(224, 224, 224, 1'}}/>
                                    <EditedRow section={this.getNewSection()} removeNewSection={this.removeNewSection}/>
                                </TableRow>
                            }

                            <TableRow>
                                <TableCell className={classes.headerCell} colSpan={isCanEdit ? 3 : 2}> Всего </TableCell>
                                <TableCell className={classes.headerCell}>{totalContactWorkHours}</TableCell>
                                <TableCell className={classes.headerCell}>{totalLectureClassesHours}</TableCell>
                                <TableCell className={classes.headerCell}>{totalLaboratoryClassesHours}</TableCell>
                                <TableCell className={classes.headerCell}>{totalPracticalClassesHours}</TableCell>
                                <TableCell className={classes.headerCell}>{totalSPOHours}</TableCell>
                                <TableCell className={classes.headerCell}>{totalTotalHours}</TableCell>
                                {isCanEdit && <TableCell className={classes.headerCell} />}
                            </TableRow>
                        </Table>
                    </Scrollbars>
                </TableContainer>

                {!createNewSectionMode && isCanEdit
                    && <Fab color="secondary"
                            className={classes.addIcon}
                            onClick={this.handleCreateNewSection}
                        >
                        <AddIcon/>
                    </Fab>
                }
            </div>
        );
    }
}

const DragHandle = SortableHandle(() => <DragIndicatorIcon style={{cursor: "pointer"}}/>);

// @ts-ignore
const SortableItem = SortableElement(({section, removeNewSection, isCanEdit}) =>
    <TableRow>
        {isCanEdit &&
        <TableCell style={{backgroundColor: '#fff', border: '1px solid rgba(224, 224, 224, 1)'}}>
            <DragHandle/>
        </TableCell>
        }
        <EditedRow section={section} removeNewSection={removeNewSection} />
    </TableRow>
);

// @ts-ignore
const SortableList = SortableContainer(({sections, removeNewSection, isCanEdit}) => {
    return (<TableBody>
            {sections.map((value: any, index: number) => (
                <SortableItem key={`item-${value.id}`}
                              index={index}
                              section={value}
                              removeNewSection={removeNewSection}
                              isCanEdit={isCanEdit}
                />
            ))}
        </TableBody>
    );
});

// @ts-ignore
export default connect(withStyles(styles)(Sections));
