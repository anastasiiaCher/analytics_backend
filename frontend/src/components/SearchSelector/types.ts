import {WithStyles} from "@material-ui/core";
import styles from "./SearchSelector.styles";
import {ReactText} from "react";

export interface SearchSelectorProps extends WithStyles<typeof styles> {
    changeSearchText: Function;
    changeItem: Function;
    label: string;
    value: string;
    valueLabel: string;
    list: SelectorListType;
    className?: string;
    disabled?: boolean;
}

export type SelectorListType = Array<SelectorItemType>;

export type SelectorItemType = {
    label: string;
    value: ReactText;
}