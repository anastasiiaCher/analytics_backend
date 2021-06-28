import { createStyles, makeStyles, Theme } from '@material-ui/core'

export const useStyles = makeStyles((theme: Theme) => createStyles({
  dialog: {
    padding: 20,
  },
  marginBottom30: {
    marginBottom: '30px'
  },
  actions: {
    marginTop: '30px'
  },
  title: {
    padding: 0,
    marginBottom: '30px'
  }
}))