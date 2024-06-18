import { FunctionComponent } from "react";
import Frame1 from "../components/Frame1";
import Frame from "../components/Frame";
import styles from "./CooksWireframe.module.css";

const CooksWireframe: FunctionComponent = () => {
  return (
    <div className={styles.cooksWireframe}>
      <div className={styles.footer}>
        <div className={styles.background} />
        <div className={styles.frame}>
          <div className={styles.frameChild} />
          <div className={styles.frameItem} />
          <div className={styles.frameInner} />
        </div>
      </div>
      <Frame1 />
      <Frame />
    </div>
  );
};

export default CooksWireframe;
