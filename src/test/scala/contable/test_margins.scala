package contable

import org.scalatest._
import breeze.linalg._

class TestMargins extends FunSpec {

  def m1 = new Margins(DenseVector(2,2,2,2),DenseVector(2,2,2,2))
  def m2 = new Margins(DenseVector(Range(0,5).toArray),DenseVector(Range(0,5).toArray))
  def m3 = new Margins(DenseVector(),DenseVector())
  def m4 = new Margins(DenseVector.fill[Int](4)(3), DenseVector.fill[Int](6)(2))
  def m5 = new Margins(DenseVector(3,1,3),DenseVector(2,3,4))
  def m6 = new Margins(DenseVector(10),DenseVector(Range(1,5).toArray))

  describe("A Margins") {
    it("should correctly determine feasibility") {
      assert(m1.isFeasible)
      assert(m2.isFeasible)
      assert(!m3.isFeasible)
      assert(m4.isFeasible)
      assert(!m5.isFeasible)
      assert(m6.isFeasible)
    }
  }
}
