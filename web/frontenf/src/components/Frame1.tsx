import { FunctionComponent } from "react";
import styles from "./Frame1.module.css";

export type Frame1Type = {
  className?: string;
};

const Frame1: FunctionComponent<Frame1Type> = ({ className = "" }) => {
  return (
    <section className={[styles.frame, className].join(" ")}>
      <div className={styles.content}>
        <div className={styles.row}>
          <div className={styles.column}>
            <div className={styles.component}>
              <img className={styles.subtractIcon} alt="" src="/subtract.svg" />
              <div className={styles.circle} />
            </div>
            <div className={styles.content1}>
              <div className={styles.actions}>
                <div className={styles.button} />
                <div className={styles.buttonSecondary} />
                <div className={styles.buttonTertiary} />
              </div>
            </div>
          </div>
        </div>
        <img className={styles.asideIcon} alt="" src="/aside.svg" />
      </div>
      <div className={styles.main}>
        <div className={styles.content2}>
          <div className={styles.row1}>
            <div className={styles.column1}>
              <img
                className={styles.subtractIcon1}
                alt=""
                src="/subtract.svg"
              />
              <div className={styles.circle1} />
            </div>
            <div className={styles.content3}>
              <div className={styles.actions1}>
                <div className={styles.button1} />
                <div className={styles.buttonSecondary1} />
                <div className={styles.buttonTertiary1} />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.content4}>
          <img className={styles.rowIcon} alt="" src="/frame-1.svg" />
          <img className={styles.actionsColumnIcon} alt="" src="/frame-2.svg" />
          <img className={styles.contentIcon} alt="" src="/frame-3.svg" />
        </div>
        <div className={styles.content5}>
          <div className={styles.row2}>
            <div className={styles.column2}>
              <img
                className={styles.subtractIcon2}
                alt=""
                src="/subtract.svg"
              />
              <div className={styles.circle2} />
            </div>
            <div className={styles.content6}>
              <div className={styles.actions2}>
                <div className={styles.button2} />
                <div className={styles.buttonSecondary2} />
                <div className={styles.buttonTertiary2} />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.content7}>
          <img className={styles.rowIcon1} alt="" src="/frame-4.svg" />
          <img className={styles.columnIcon} alt="" src="/frame-5.svg" />
        </div>
        <div className={styles.content8}>
          <img className={styles.rowIcon2} alt="" src="/frame-6.svg" />
          <img
            className={styles.columnIcon1}
            loading="lazy"
            alt=""
            src="/frame-7.svg"
          />
        </div>
        <div className={styles.content9}>
          <div className={styles.row3}>
            <div className={styles.column3}>
              <img
                className={styles.subtractIcon3}
                rows={11}
                cols={15}
                alt=""
                src="/subtract.svg"
              />
              <div className={styles.circle3} />
            </div>
            <div className={styles.content10}>
              <div className={styles.actions3}>
                <div className={styles.button3} />
                <div className={styles.buttonSecondary3} />
                <div className={styles.buttonTertiary3} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Frame1;
