package contable

import breeze.linalg._
import breeze.numerics._
import scala.annotation.tailrec
import scala.math

abstract class Sampler(marg: Margins) {

  val margins: Margins = marg

  def sample: DenseMatrix[Int]

  def samples(n: Int): List[DenseMatrix[Int]] = {
    @tailrec def sample_acc(n: Int, acc: List[DenseMatrix[Int]]): List[DenseMatrix[Int]] = n match {
      case 0 => acc
      case x if x<0 => acc
      case x => sample_acc(x-1, sample :: acc)
    }
    sample_acc(n,List())
  }

  @tailrec final def rejectionSample(maxIter:Int = 100): Option[DenseMatrix[Int]] = {
    if(maxIter <= 0){ None }

    val X = sample
    if (margins.check(X)) { Some(X) }
    else { rejectionSample(maxIter - 1) }
  }
}

class BoundedExactRowsExpectedColumns(marg: MarginsWithCellBounds) extends Sampler(marg) {

  override val margins: MarginsWithCellBounds = marg

  def sample: DenseMatrix[Int] = DenseMatrix.zeros[Int](0,0)

  protected def computeTable(w: List[Double], k: Int, b: List[Int]): List[List[Double]] = {

    //Note: could compute the transpose of the table slightly more efficiently
    val wpow = (1 to k).scan(1.0)( (x: Double, y:Int) => w * x )
    def oneStep(wi : Double, v : List[Double], cellBound: Int):List[Double] = {
      for( ii <- 0 to (k+1) ) yield { (v.slice(ii - math.min(ii,cellBound), ii+1).
        reverse.
        zip(wpow).
        map(_ * _).
        sum)}

    }

  }
}
