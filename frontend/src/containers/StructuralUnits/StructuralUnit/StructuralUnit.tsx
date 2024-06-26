import React from 'react';
import get from 'lodash/get';

import Scrollbars from "react-custom-scrollbars-2";
import classNames from 'classnames';

import Paper from '@mui/material/Paper';
import Fab from "@mui/material/Fab";
import Typography from "@mui/material/Typography";

import {withStyles} from '@mui/styles';

import AddIcon from "@mui/icons-material/Add";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/DeleteOutlined";
import EditIcon from "@mui/icons-material/EditOutlined";

import ConfirmDialog from "../../../components/ConfirmDialog";

import {positionsListObject} from "./constants";
import {getUserFullName} from "../../../common/utils";

import {structuralUnitUserType} from '../types';
import {structuralUnitFields, structuralUnitUserFields} from "../enum";
import CreateModal from "./CreateModal";
import {withRouter} from "../../../hoc/WithRouter";

import connect from './StructuralUnit.connect';
import styles from './StructuralUnit.styles';

class StructuralUnit extends React.Component<any> {
  state = {
    deleteConfirmId: null
  }

  componentDidMount() {
    this.props.actions.getStructuralUnit(this.getStructuralUnitId());
  }

  getStructuralUnitId = () => parseInt(get(this, 'props.params.id', '0'));

  handleClickDelete = (id: number) => () => {
    this.setState({
      deleteConfirmId: id
    });
  }

  handleConfirmDeleteDialog = () => {
    const {deleteConfirmId} = this.state;

    this.props.actions.removeUserFromStructuralUnit({
      userId: deleteConfirmId,
      id: this.getStructuralUnitId()
    });

    this.closeConfirmDeleteDialog();
  }

  closeConfirmDeleteDialog = () => {
    this.setState({
      deleteConfirmId: null
    });
  }

  handleClickEdit = (item: structuralUnitUserType) => () => {
    this.props.actions.openDialog(item);
  }

  handleCreate = () => {
    this.props.actions.openDialog({
      [structuralUnitUserFields.STRUCTURAL_UNIT]: this.getStructuralUnitId(),
    });
  }

  render() {
    //@ts-ignore
    const {classes} = this.props;
    const {structuralUnit} = this.props;
    const {deleteConfirmId} = this.state;

    return (
      <Paper className={classes.root}>
        <Typography className={classes.title}>
          Сотрудники структурного подразделения «{get(structuralUnit, structuralUnitFields.TITLE, '')}»
        </Typography>

        <div className={classes.tableWrap}>
          <div className={classNames(classes.listItem, classes.header)}>
            <Typography className={classNames(classes.marginRight, classes.titleCell)}>
              ФИО
            </Typography>
            <Typography className={classNames(classes.marginRight, classes.roleCell)}>
              Должность
            </Typography>
          </div>

          <div className={classes.list}>
            <Scrollbars>
              {structuralUnit[structuralUnitFields.USERS]?.map((item: structuralUnitUserType) => {
                //@ts-ignore
                const position = positionsListObject[item[structuralUnitUserFields.STATUS]];
                return <div className={classes.listItem} key={item[structuralUnitUserFields.ID]}>
                  <Typography className={classNames(classes.marginRight, classes.titleCell)}>
                    {getUserFullName(item[structuralUnitUserFields.USER])}
                  </Typography>
                  <Typography className={classNames(classes.marginRight, classes.roleCell)}>
                    {position}
                  </Typography>
                  <div className={classes.actions}>
                    <IconButton onClick={this.handleClickDelete(item[structuralUnitUserFields.ID])}>
                      <DeleteIcon/>
                    </IconButton>
                    <IconButton onClick={this.handleClickEdit(item)}>
                      <EditIcon />
                    </IconButton>
                  </div>
                </div>;
              })}
            </Scrollbars>
          </div>
        </div>

        <Fab color="secondary"
             classes={{
               root: classes.addIcon
             }}
             onClick={this.handleCreate}
        >
          <AddIcon/>
        </Fab>

        <ConfirmDialog onConfirm={this.handleConfirmDeleteDialog}
                       onDismiss={this.closeConfirmDeleteDialog}
                       confirmText={'Вы точно уверены, что хотите удалить сотрудника из подразделения?'}
                       isOpen={Boolean(deleteConfirmId)}
                       dialogTitle={'Удалить сотрудника'}
                       confirmButtonText={'Удалить'}
        />

        <CreateModal />
      </Paper>
    );
  }
}

//@ts-ignore
export default connect(withStyles(styles)(withRouter(StructuralUnit)));
